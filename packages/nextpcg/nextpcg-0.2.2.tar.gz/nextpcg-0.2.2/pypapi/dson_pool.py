# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import threading
import asyncio
import subprocess
from typing import Dict

from .meta_helper import Singleton
from .dson import DsonMetaInfo
from .plugin_protocol import server_check_done


class DsonPool(metaclass=Singleton):
    """a asyncpool

    maintain connection to plugins, 
    dispatch task to the plugin
    resolve thread race
    """

    def __init__(self, plugin_max, worker_count, max_task_time, logger):
        """initialize the pool
        
        Args:
            plugin_count (int): number of max plugin running.
            max_task_time (int): max running time of a plugin per task
        """
        self._plugins = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        self._lock_create_lock = threading.Lock()
        self._plugin_max = plugin_max
        self._worker_count = worker_count
        self._loop = asyncio.new_event_loop()
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self._max_task_time = max_task_time
        self._workers = None
        self.logger = logger
        self.dson_script_name = ''
        if os.name == 'posix':
            self.dson_script_name = 'dson_init.sh'
        else:
            self.dson_script_name = 'dson_init.bat'

    def run_task_consumer_on_background(self):
        """run task consumer on background thread"""
        t = threading.Thread(name='dson_plugin_pool', target=self.__loop_in_thread, args=(self._loop,self.run_on_task_producer_async(None)))
        t.start()

    def enqueue_task(self, task, json_error_data, *args):
        """enqueue a session task into session pool
        
        Args:
            task (func): a plugin task to run
            *args: arguments pass to this task
        """
        event = threading.Event()
        self.logger.debug(f'enqueue task {task} with param {args}')
        self._loop.call_soon_threadsafe(self.task_queue.put_nowait, (event, task, json_error_data, *args))
        return event

    def __loop_in_thread(self, loop, task):
        asyncio.set_event_loop(loop)
        self.task_queue = asyncio.Queue()
        loop.run_until_complete(task)

    async def run_on_task_producer_async(self, producer):
        """run a task producer and consuming task with plugin pool async"""
        assert self._loop==self.task_queue._loop, f"hei{self._loop} {self.task_queue._loop}"

        self._workers = [asyncio.create_task(self.__worker_loop(i)) for i in range(self._worker_count)]
        
        if producer is None:
            await asyncio.gather(*self._workers, return_exceptions=False)
        else:
            task_producer = asyncio.create_task(producer())
            await asyncio.gather(*self._workers, task_producer, return_exceptions=True)

    async def __worker_loop(self, i):
        """a consumer woker
        ref: https://github.com/CaliDog/asyncpool

        Args:
            i: id of worker
        """
        while True:
            got_obj = False
            got_exception = True

            try:
                event, task_to_proceed, json_error_data, *args = await self.task_queue.get()
                got_obj = True

                # get or pull the plugin
                plugin_name = args[0].plugin_name # args[0] should be a DsonMetaInfo
                proc, lock = await self.get_plugin(args[0])
                await lock.acquire() # plugin lock
                running_coro = asyncio.wait_for(task_to_proceed(proc, *args), self._max_task_time, loop=self._loop)
                await running_coro
            except asyncio.CancelledError as e:
                self.logger.info(f'Worker {i} is Cancelled')
                break
            except asyncio.TimeoutError as e:
                json_error_data['Error_Tag'] = 'dson plugin error'
                json_error_data['Error_Info'] = f'plugin time out, max task time {self._max_task_time}'
                self.logger.warning(f'plugin time out, max task time {self._max_task_time}')
            except KeyboardInterrupt as e:
                self.logger.info(f"Worker {i} is Interrupt")
                break
            except (MemoryError, SystemError) as e:
                self.logger.exception(e)
                raise
            except ProcessLookupError as e:
                self.logger.exception(e)
            except BaseException as e:
                self.logger.exception(e)
                self.logger.exception(f"Worker {i} Call Failed")
                # raise
            else:
                got_exception = False
            finally:
                if got_obj:
                    event.set() # inform that task is done
                    self.task_queue.task_done()
                if got_exception:
                    # if exception, del the plugin in case plugin is still running but no one is expecting the result
                    try:
                        proc.terminate()
                        lock.release()
                        del self._plugins[plugin_name]
                        del self._locks[plugin_name]
                        self.logger.warning(f'plugin {plugin_name} is terminated')
                    except BaseException as e:
                        pass
                else:
                    try:
                        lock.release()
                    except BaseException as e:
                        pass

    async def get_plugin(self, dson_meta_info: DsonMetaInfo):
        assert dson_meta_info.if_in_server==False
        plugin_name = dson_meta_info.plugin_name
        if plugin_name == None:
            raise Exception('expect plugin_name bug get None')
        # get lock
        # if plugin_name not in self._locks:
            # with self._lock_create_lock:
            #     self.__loop_in_thread[plugin_name] = threading.Lock()
            # lock = self._locks[plugin_name]
        if plugin_name not in self._plugins:
            plugin_path = os.path.join(os.getenv('PYTHONPROJECT_PATH'), plugin_name).replace('\\', '/')
            bash_path = os.path.join(plugin_path, '.nextpcg', self.dson_script_name).replace('\\', '/')
            proc = subprocess.Popen([bash_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            self.logger.info(f'new dson plugin: {plugin_name}')
            self._plugins[plugin_name] = proc
            lock = asyncio.Lock()
            self._locks[plugin_name] = lock
            await lock.acquire()
            await server_check_done(proc, self.logger) # ensure that await is after inserting proc to _plugins
            lock.release()
        else:
            proc = self._plugins[plugin_name]
            lock = self._locks[plugin_name]
        return proc, lock
        

def DsonTask(task):
    """a decorator for nextpcg python plugin task"""
    async def wrapper(*args, **kwargs):
        assert isinstance(args[0], subprocess.Popen), f"{task}'s first parameter should be Popen"
        assert isinstance(args[1], DsonMetaInfo), f"{task}'s second parameter should be DsonMetaInfo"
        await task(*args, **kwargs)
    return wrapper