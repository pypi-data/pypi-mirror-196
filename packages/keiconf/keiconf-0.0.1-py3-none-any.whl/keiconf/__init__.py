# SPDX-FileCopyrightText: 2023-present Charles C. <nafredy@gmail.com>
#
# SPDX-License-Identifier: MIT
from typing import Any, Union
from threading import Lock, Thread, Event
from pathlib import Path
import json

_CHANGE_WATCH_INTERVAL=1

class KeiConf:
    '''
    A minimalist application json configuration tool with file watches
    for the developer who just wants to get going
    '''
    
    _exit = Event
    _filepath: Path
    _json_indent: int
    _fail_on_missing_key: bool
    _create_if_not_exist: bool
    _watch_for_changes: bool
    _watcher: Thread
    _conf = {}
    _last_modified: float
    _lock: Lock # locks the _conf
    _file_lock: Lock # locks the _filepath
    _modified_lock: Lock # locks the _last_modified
    _watcher_lock: Lock # locks the watcher and watch bool
    
    def __init__(self, filepath: Union[str, Path], indent: int = 2, \
                fail_on_missing_key: bool = False, create_if_not_exist: bool = False, \
                watch_for_changes: bool = False):
        '''
        Initialize the configuration interface
        
        :param [str|Path] filepath: The /path/to/file.json where the config file is or should be
        :param int indent: The json indent to use in the written file
        :param bool fail_on_missing_key: Raises KeyError if requested config key does not exist, False just returns None
        :param bool create_if_not_exist: Creates the given filepath if it does not exist (including directory tree)
        :raises TypeError: if the filepath is not str or Path
        :raises TypeError: if the indent is not int
        :raises TypeError: if the fail_on_missing_key is not bool
        :rasised TypeError: if the create_if_not_exist is not bool
        '''
        self._lock = Lock()
        self._file_lock = Lock()
        self._modified_lock = Lock()
        self._watcher_lock = Lock()
        self._exit = Event()
        
        if isinstance(filepath, str):
            self._filepath = Path(filepath)
        elif isinstance(filepath, Path):
            self._filepath = filepath
        else:
            raise TypeError(f'expected filepath to be (str | Path), got {type(filepath)}')
        
        self.__class__.__check_filepath_is_dir(self._filepath)
        
        if isinstance(indent, int):
            self._json_indent = indent
        else:
            raise TypeError(f'expected indent to be (int), got {type(indent)}')
    
        if isinstance(fail_on_missing_key, bool):
            self._fail_on_missing_key = fail_on_missing_key
        else:
            raise TypeError(f'expected fail_on_missing_key to be (bool), got {type(fail_on_missing_key)}')
        
        if isinstance(create_if_not_exist, bool):
            self._create_if_not_exist = create_if_not_exist
        else:
            raise TypeError(f'expected create_if_not_exist to be (bool), got {type(create_if_not_exist)}')
    

        if isinstance(watch_for_changes, bool):
            self._watch_for_changes = watch_for_changes
        else:
            raise TypeError(f'expected watch_for_changes to be (bool), got {type(watch_for_changes)}')
    
        self.__create_config_if_not_exist()
        self.__load_config()
        
        
        if self._watch_for_changes:
            self.__start_watcher()
    
    def get(self, keys: str) -> Any:
        '''
        Get the value of a key given format get("path.to.thing")
        '''
        if not isinstance(keys, str):
            raise TypeError(f'expected keys to be str but got {type(keys)}: {keys}')
        
        paths = keys.split(".")
        result = self.__class__.__gattr(self._conf, paths)
        if result == "" and self._fail_on_missing_key:
            raise KeyError(f'key {keys} does not exist in config')
        
        return result
    
    def is_watching(self) -> bool:
        return self._watch_for_changes
    
    def stop(self):
        '''
        Stops the config file watcher
        '''
        self.__stop_watcher()
    
    def start(self):
        '''
        Starts the config file watcher
        '''
        self.__create_watcher()
        self.__start_watcher()
    
    @staticmethod
    def __gattr(d: dict, keys: list[str]) -> Any:
        '''
        Return the value of a nested dict key, using a list of keys
        ordered by depth
        '''
        if not isinstance(d, dict):
            raise TypeError(f"expected d to be dict but got {type(d)}: {d}")
        
        if not isinstance(keys, list):
            raise TypeError(f"expected keys to be list[str] but got {type(keys)}: {keys}")
        
        try:
            for k in keys:
                d = d[k]
            return d
        except KeyError as e:
            raise KeyError(e)
    
    def __create_watcher(self):
        '''
        Creates a new watcher
        '''
        
        try:
            if self._watcher.is_alive():
                self.__stop_watcher()
                self._watcher.join() # TODO: very quickly timeout
            self._watcher_lock.acquire()
            self._watcher = Thread(name="config_file_watcher", target=self.__watch_config, daemon=True)
            self._watcher_lock.release()
        except AttributeError:
            self._watcher_lock.acquire()
            self._watcher = Thread(name="config_file_watcher", target=self.__watch_config, daemon=True)
            self._watcher_lock.release()
        
        
    
    def __start_watcher(self):
        '''
        Starts the config file watcher
        '''
        self._watcher_lock.acquire()
        self._exit.clear()
        self._watch_for_changes = True
        self._watcher.start()
        self._watcher_lock.release()
    
    def __stop_watcher(self):
        '''
        Stops the config file watcher
        '''
        self._watcher_lock.acquire()
        self._exit.set()
        self._watch_for_changes = False
        self._watcher_lock.release()
    
    def __watch_config(self):
        '''
        Watches the given config file for changes and automatically loads them
        If the load fails to read or parse it will raise a warning but preserve
        the current working configuration.
        '''
        while not self._exit.is_set():
            self.__check_config_for_changes()
            self._exit.wait(_CHANGE_WATCH_INTERVAL)
        
    def __check_config_for_changes(self):
        '''
        Naive check if the file has been modified and loads it if it has
        '''
        modified = self._filepath.lstat().st_mtime
        if modified != self._last_modified:
            self._modified_lock.acquire()
            self._last_modified = modified
            self._modified_lock.release()
            self.__load_config()
    
    def __load_config(self):
        '''
        Read the configfile into memory
        '''
        self._file_lock.acquire()
        self._lock.acquire()
        with open(self._filepath, 'r') as file:
            self._conf = json.load(file)
        self._file_lock.release()
        self._lock.release()
        
        self.__set_last_modified()
        
    def __create_config_if_not_exist(self):
        '''
        If __create_if_not_exist, creates the config file and its directory tree 
        if it doesn't exist
        '''
        
        if self._create_if_not_exist and not self._filepath.is_file():
            self.__create_config_directory()
            self.__write()
    
    def __set_last_modified(self):
        '''
        Update the last modified of the config file
        '''
        self._modified_lock.acquire()
        self._last_modified = self._filepath.lstat().st_mtime
        self._modified_lock.release()
    
    def __create_config_directory(self):
        '''
        creates the config path directories
        '''
        self._file_lock.acquire()
        self._filepath.parents[0].mkdir(parents=True, exist_ok=True)
        self._file_lock.release()
    
    def __write(self):
        '''
        Write KeiConf config file to disk
        '''
        self._file_lock.acquire()
        self._filepath.write_text(str(self))
        self._file_lock.release()
        
        self.__set_last_modified()
    
    def __str__(self) -> str:
        return json.dumps(self._conf, indent=self._json_indent)
    
    @staticmethod
    def __check_filepath_is_dir(path: Path):
        if path.is_dir():
            raise IsADirectoryError(f'given filepath {path} is a directory, expected path/to/file.json')
