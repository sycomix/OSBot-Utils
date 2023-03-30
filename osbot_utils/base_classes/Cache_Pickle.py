import os
from functools import wraps

from osbot_utils.utils.Files import path_combine, folder_create, temp_folder_current, file_exists, pickle_load_from_file, pickle_save_to_file

FOLDER_CACHE_ROOT_FOLDER = '_cache_pickle'

class Cache_Pickle:

    def __init__(self):
        self.cache_enabled = True
        self.cache_setup()              # make sure the cache folder exists

    def __getattribute__(self, name):
        if name.startswith('cache_') or name.startswith('__'):
            return super().__getattribute__(name)

        target_method = super().__getattribute__(name)
        if not callable(target_method):
            raise AttributeError(f"{name} is not a callable method")

        return self.cache_data(target_method)

    def cache_clear(self):
        cache_dir = self.cache_path()
        for filename in os.listdir(cache_dir):
            if filename.endswith('.pickle'):
                os.remove(os.path.join(cache_dir, filename))
        return self

    def cache_data(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            caller_name = func.__name__

            path_file = path_combine(self.cache_path(), f'{caller_name}.pickle')
            if 'reload_cache' in kwargs:                                        # if the reload parameter is set to True
                reload_cache = kwargs['reload_cache']                           # set reload to the value provided
                del kwargs['reload_cache']                                      # remove the reload parameter from the kwargs
            else:
                reload_cache = False                                            # otherwise set reload to False

            if 'use_cache' in kwargs:
                use_cache = kwargs['use_cache']
                del kwargs['use_cache']
            else:
                use_cache = True

            if use_cache is True and reload_cache is False and file_exists(path_file):
                return pickle_load_from_file(path_file)
            else:
                data = func(*args, **kwargs)
                if data and use_cache is True:
                    pickle_save_to_file(data, path_file)
                return data
        return wrapper

    def cache_disable(self):
        self.cache_enabled = False

    def cache_path(self):
        module_name = self.__class__.__module__
        folder_name = f'{FOLDER_CACHE_ROOT_FOLDER}/{module_name.replace(".", "/")}'
        return path_combine(temp_folder_current(), folder_name)


    def cache_setup(self):
        folder_create(self.cache_path())
        return self
