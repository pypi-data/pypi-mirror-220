from orbit_component_base.src.orbit_plugin import PluginBase, ArgsBase
from orbit_component_base.src.orbit_decorators import Sentry, check_permission
from orbit_component_zerodocs.schema.Cache import CacheCollection
from orbit_component_zerodocs.schema.APIs import APIsCollection
from orbit_component_zerodocs.schema.Project import ProjectCollection
from asyncinotify import Inotify, Mask
from loguru import logger as log
from asyncio import sleep, create_task
import os


class Plugin (PluginBase):

    NAMESPACE = 'zerodocs'
    COLLECTIONS = [
        CacheCollection,
        APIsCollection,
        ProjectCollection
    ]

    @Sentry()
    async def on_cache_fetch (self, sid, params, force=False):
        return await CacheCollection(sid).fetch(params, force)

    @Sentry()
    async def on_get_project_id (self, sid, params):
        return await CacheCollection(sid).get_project_id(params)

    @Sentry()
    async def on_get_api_remote (self, sid, provider, api, branch, path):
        return APIsCollection(sid).get_api_remote(provider, api, branch, path)

    @Sentry ()
    async def on_search (self, sid, text):
        return await CacheCollection(sid).search(text)

    @Sentry(check_permission, NAMESPACE, 'User is allowed to update an existing project')
    async def on_cache_put (self, sid, params):
        return await CacheCollection(sid).put(params)

    @Sentry(check_permission, NAMESPACE, 'User is allowed to add a new project')
    async def on_project_put (self, sid, params):
        return await ProjectCollection(sid).put(params)

    @Sentry(check_permission, NAMESPACE, 'User is allowed to delete an existing project')
    async def on_project_remove (self, sid, params):
        try:
            # log.error(f"Running delete: {params}")
            await ProjectCollection(sid).remove(params)
            await CacheCollection(sid).remove(params)
            return {'ok': True}
        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}


class Args (ArgsBase):
        
    def setup (self):
        self._parser.add_argument("--zd-follow", nargs=5, type=str, help='Map a local source path unto the cache for previewing', metavar="(PATH, API, PROVIDER, PROJECT, BRANCH)")
        return self
    
       
class Tasks (ArgsBase):
    
    async def process (self):
         
        async def watcher ():
            log.success("[ZD File watcher running]")
            base, api, provider, project, branch = self._args.zd_follow
            with Inotify() as inotify:
                for path, _, _ in os.walk(base):
                    inotify.add_watch(path, Mask.MODIFY)
                async for event in inotify:
                    try:
                        log.debug(f'Local file change in "{event.name}" triggered cache refresh [{event.path}]')
                        with open(event.path, 'r') as io:
                            text = io.read()
                        path =  str(event.path)[len(base):]
                        if path.startswith('/'):
                            path = path[1:]
                        params = {
                            'root': api,
                            'provider': provider,
                            'project': project, 
                            'branch': branch,
                            'path': path
                        }
                        await CacheCollection().local_update(params, text)
                    except FileNotFoundError:
                        log.debug(f'File not found: {event.path}')
                    except Exception as e:
                        log.exception(e)
                        
        if self._args.zd_follow:
            create_task (watcher())
