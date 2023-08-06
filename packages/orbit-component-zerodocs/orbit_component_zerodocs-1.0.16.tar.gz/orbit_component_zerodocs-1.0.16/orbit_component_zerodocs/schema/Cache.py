from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection, register_class, register_method
from orbit_component_zerodocs.doc_python import Documentation
from orbit_database import SerialiserType, Doc
from hashlib import md5
from orbit_component_base.src.orbit_shared import world
from loguru import logger as log
from gitlab import Gitlab
from gitlab.exceptions import GitlabHeadError
from base64 import b64decode
from asyncio import ensure_future
from datetime import datetime
from cmarkgfm import github_flavored_markdown_to_html
from cmarkgfm.cmark import Options as opts
from asyncio import ensure_future
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from bs4 import BeautifulSoup
from asyncio import get_running_loop as loop
from orbit_component_zerodocs.schema.Project import ProjectTable
from re import sub as substitute
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from io import StringIO
import tokenize

STOP = set(stopwords.words('english'))
STOP.add('none')

gitlab = Gitlab()
remove_whitespace = {ord('\r'): 32, ord('\n'): 32, ord('\t'): 32}


class CacheTable (BaseTable):

    norm_table_name = 'cache'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        {'index_name': 'by_params'  , 'duplicates': False, 'func': '{root}|{provider}|{project}|{branch}|{path}'},
        {'index_name': 'by_root'    , 'duplicates': True, 'func': '{root}|{path}'},
        {'index_name': 'by_words'   , 'iwx': True }
    ]

    def _cache_path (self, name):
        # log.warning(f"Construct: {self._provider}|{self._project}|{self._path}|{name}")
        return world.conf.tmp / md5(f'{self._provider}|{self._project}|{self._path}|{name}'.encode()).hexdigest()

    def from_cache (self, params):
        result = {'ok': True, 'loading': True, '_id': self.key, 'stamp': 0}
        for mode in params.get('modes', ['html']):
            try:
                with open(self._cache_path(mode), 'r') as io:
                    result[mode] = io.read()
                    result['loading'] = False
                    result['stamp'] = self._stamp
            except FileNotFoundError:
                if mode == 'html':
                    log.warning(f'Missing: {self._cache_path(mode)}')
                    self._refresh = True
                    self.save()
        return result

    async def fetch (self):
        return await loop().run_in_executor(None, self.thread_fetch)

    async def head (self):
        return await loop().run_in_executor(None, self.thread_head)

    def thread_fetch (self):
        try:
            project = gitlab.projects.get(self._project_id)
            if not project:
                raise Exception(f'unknown project id: {self._project_id}')
            log.error(f"Get, ref={self._branch}")
            data = project.files.get(self._path, ref=self._branch)
            if not data:
                raise Exception(f'unable to find path: {self._provider}/{self._path}')
            self._badges = [(badge.rendered_link_url, badge.rendered_image_url) for badge in project.badges.list()]
            return b64decode(data.content) if data.encoding == 'base64' else data.content
        except Exception as e:
            log.exception(e)

    def thread_head (self):
        try:
            project = gitlab.projects.get(self._project_id)
            if not project:
                raise Exception(f'unknown project id: {self._project_id}')
            log.error(f"Head, path={self._path}, ref={self._branch}")
            data = project.files.head(self._path, ref=self._branch)
            if not data:
                raise Exception(f'unable to find path: {self._provider}/{self._path}')
            return data
        except GitlabHeadError:
            log.error(f'Unable to find proj={self._project_id} prov={self._provider} path={self._path}')
        except Exception as e:
            log.exception(e)

    def from_params (self, params, transaction=None):
        doc = Doc(params)
        self.set(self.norm_tb.seek_one('by_params', doc, txn=transaction))
        if not self.isValid:
            self.set(doc)
            # log.error(f'Missing doc: {doc.doc}')
        return self


@register_class
class CacheCollection (BaseCollection):

    table_class = CacheTable
    table_methods = []

    MD_OPTIONS = (opts.CMARK_OPT_UNSAFE | opts.CMARK_OPT_LIBERAL_HTML_TAG | opts.CMARK_OPT_DEFAULT)

    async def search (self, text):
        ids = []
        text = text.split(' ')
        if not len(text):
            return {'ok': True, 'count': 0}
        
        words = text[:-1]
        matches = self.table_class().norm_tb.lexicon('by_words', text, 9999)
        if len(matches):
            word, count = matches[0]
            words.append(word)

        if not len(words):
            return {'ok': True, 'count': 0}

        count, results = self.table_class().norm_tb.match('by_words', words)
        if not count:
            return {'ok': True, 'count': 0}
        
        for oid in results:
            ids.append(oid.decode())
        
        return {'ok': True, 'ids': ids, 'count': count, 'partial': words, 'matches': [word[0] for word in matches]}

    async def local_update (self, params, text):
        doc = self.table_class().from_params(params)
        if doc.isValid:
            return await self.update(doc, text)

    async def fetch (self, params, force=False):
        # log.error(f'Force={force}')
        doc = self.table_class().from_params(params)
        if not doc.isValid:
            ensure_future(self.check(doc))
        # log.success(f'Doc={doc.doc}, {doc.isValid}')
        if force:
            doc._etag = None
        ret = doc.from_cache(params)
        if doc.isValid and doc._refresh:
            ensure_future(self.check(doc))
        return ret

    async def update (self, doc, text):
        if text and isinstance(text, bytes): text = text.decode()
        # log.error(f"Open: {doc._cache_path('text')}")
        with open(doc._cache_path('text'), 'w') as io:
            io.write(text)
        if doc._path.endswith('.md') or doc._label in ['LICENSE', 'README']:
            html = github_flavored_markdown_to_html(text, self.MD_OPTIONS)
            formatter = HtmlFormatter(style='manni')
            soup = BeautifulSoup(html, 'html.parser')
            
            text = " ".join(soup.get_text(separator=" ").translate(remove_whitespace).split()).strip()
            text = word_tokenize(substitute(r'&\w+;\s?', '', substitute('[^0-9a-zA-Z]+', ' ', text).lower().strip()))
            doc.words = Counter([word for word in filter(lambda word: len(word) > 1 and word not in STOP, text)])

            for tag in soup.find_all('pre'):
                try:
                    lexer = get_lexer_by_name(tag.get('lang'), stripall=True)
                    tag.replace_with(BeautifulSoup(highlight(tag.find('code').text, lexer, formatter), 'html.parser'))
                except ClassNotFound:
                    pass
            html = '<style>' + formatter.get_style_defs() + '</style>' + str(soup)
            
            for tag in soup.find_all('src'):
                ...
            
            
        else:
            try:
                lexer = get_lexer_for_filename(doc._path, stripall=True)
            except ClassNotFound:
                lexer = get_lexer_by_name('text', stripall=True)

            formatter = HtmlFormatter(style='manni', full=True, linenos='inline', classprefix="of", lineanchors='line-no')
            html = highlight(text, lexer, formatter)

        with open(doc._cache_path('html'), 'w') as io:
            io.write(html)

        if doc._path.endswith('.py'):
            index, html = Documentation().run(doc.key, text)
            doc._children = index
            formatter = HtmlFormatter(style='manni')
            soup = BeautifulSoup(html, 'html.parser')

            for tag in soup.find_all('pre'):
                try:
                    lexer = get_lexer_for_filename(doc._path, stripall=True)
                    hlight = tag.find('code')
                    if hlight:
                        tag.replace_with(BeautifulSoup(highlight(hlight.text, lexer, formatter), 'html.parser'))
                except ClassNotFound:
                    pass
                except ClassNotFound:
                    pass
            html = '<style>' + formatter.get_style_defs() + '</style>' + str(soup)

            with open(doc._cache_path('api'), 'w') as io:
                io.write(html)
                doc._children = index

            words = Counter()
            with StringIO(text) as io:
                tokens = tokenize.generate_tokens(io.readline)
                for token in tokens:
                    word = token.string.strip()
                    if not word.startswith('"') and not word.startswith("'") and not word.startswith("#"):
                        if len(word) > 1:
                            words.update([word])
                    for word in word.replace('"', '').replace("'", '').replace("\n", " ").replace('#', '').split(" "):
                        if len(word) > 1 and word[0] >= '0' and word[0] <= 'z':
                            words.update([word])
            doc.words = words
            print(words)
        doc.update({'stamp': datetime.now().timestamp()})
        doc.save() if doc.isValid else doc.append()

    async def check (self, doc):
        try:
            project = ProjectTable().from_params(doc)
            doc._project_id = project._project_id
            head = await doc.head()
            if head:
                etag = head.get('Etag')
                log.success(f'Etag={etag} Old={doc._etag}')
                if etag == doc._etag and not doc._refresh:
                    return
                log.warning(f"Check did an update, new etag={etag}, old={doc._etag}")
                doc.update({'etag': etag, 'refresh': False})
                text = await doc.fetch()
                return await self.update(doc, text)
            else:
                log.error(f'Unable to load file: {doc.doc}')
                # TODO: log an warning here to clear the client's loading flag
        except Exception as e:
            log.exception(e)

    async def get_project_id (self, params):
        if params.get('provider') == 'gitlab':
            projects = await loop().run_in_executor(None, lambda p: gitlab.projects.list(search=p), params.get('project'))
            if len(projects) == 0:
                return {'ok': False, 'error': f'Project not found: {params.get("project")}'}
            for project in projects:
                if project.path == params.get('project'):                           
                    branches = []
                    project_id = project.id
                    project = gitlab.projects.get(project_id)
                    for branch in project.branches.list():
                        branches.append(branch.name)
                    return {'ok': True, 'id': project_id, 'branches': branches }
            return {'ok': False, 'error': f'Project not found: {params.get("project")}'}
        raise Exception(f'unknown provider: {params.get("provider")}')
    
    async def put (self, params):
        old_data = params.get('old_data')
        new_data = params.get('new_data')
        # log.success(f'Create> {new_data}')
        # log.warning(f'Delete> {old_data}')
        for item in new_data:
            doc = self.table_class().from_params(item)
            if '_id' in doc:
                doc.pop('_id')
            if 'children' in doc:
                doc.pop('children')

            # if '|' in item.get('key'):
            #     item['key'] = item.get('key').split('|')[1]

            if doc.isValid:
                # log.debug(f'Update')
                doc.update(item).save()
            else:
                # log.debug(f'Append')
                doc.update(item).append()
        for item in old_data:
            doc = self.table_class().from_params(item)
            if doc:
                self.table_class().norm_tb.delete(doc.key)
            else:
                log.error(f'attempt to delete: {item} - failed')
        return {'ok': True}

    async def remove (self, params):
        root = params.get('root')
        provider = params.get('provider')
        project = params.get('project')
        branch = params.get('branch')
        limit = Doc({
            'root': root,
            'provider': provider,
            'project': project,
            'branch': branch,
            'path': ''
        })
        for result in self.filter('by_params', lower=limit):
            entry = result.doc
            if entry._provider != provider or entry._project != project or entry._root != root or entry._branch != branch:
                break
            entry.delete()

    @register_method
    def get_ids(cls, session, params, transaction=None):
        ids, data = [], []
        if 'ids' in params:
            for id in params['ids']:
                doc = cls.table_class().from_key(id)
                if doc.isValid:
                    session.append(params, doc.key, ids, data, doc, strip=cls.table_strip)
        else:
            duds = []
            limit = Doc(params.get('filter'))
            for result in cls().filter(index_name='by_root', lower=limit):
                doc = result.doc
                if doc._root != limit._root:
                    break
                if not doc._key:
                    duds.append(doc.key)
                    continue
                session.append(params, result.oid.decode(), ids, data, doc, strip=cls.table_strip)
        session.update(ids, params)
        if duds:
            log.error(f'Excluded duds: {len(duds)}')
            cls().delete(duds)
            
        return {'ok': True, 'ids': ids, 'data': data}

