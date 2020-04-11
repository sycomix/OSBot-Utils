import os

from osbot_utils.utils.Files import Files
from osbot_utils.utils.Json  import Json


def get_cache_in_tmp_key(self_obj, function_obj, params):
    class_name      = self_obj.__class__.__name__
    if function_obj.__class__.__name__ == 'str':
        function_name = function_obj
    else:
        function_name = function_obj.__name__
    if params:
        params_as_string = '_'.join(str(x) for x in params).replace('/',' ')
        return f'{class_name}_{function_name}_{params_as_string}'
    else:
        return f'{class_name}_{function_name}'

def get_cache_in_tmp_path(self_obj, function_obj, params):
    cache_key = get_cache_in_tmp_key(self_obj, function_obj, params)
    return '/tmp/cache_in_tmp_{0}.gz'.format(cache_key)

def get_cache_in_tmp_data(cache_path):
    return Json.load_json_gz(cache_path)

def save_cache_in_tmp_data(cache_path, data):
    Json.save_json_gz(cache_path,data)
    return data

# main decorator function
def cache_in_tmp_save(function):
    def wrapper(*args):
        params     = list(args)
        self_obj   = params.pop(0)
        cache_path = get_cache_in_tmp_path(self_obj, function, params)
        return save_cache_in_tmp_data(cache_path, function(*args))
    return wrapper


def cache_in_tmp(function):
    def wrapper(*args):
        params        = list(args)
        self_obj      = params.pop(0)       # todo: add support for methods without this
        cache_path    = get_cache_in_tmp_path(self_obj, function, params)
        data          = get_cache_in_tmp_data(cache_path)
        if data:
            return data
        return save_cache_in_tmp_data(cache_path,function(*args))

    return wrapper

# todo: find better folder to hold this type of helpers
def cache_in_tmp_clear(function):
    def wrapper(*args):
        params = list(args)
        self_obj = params.pop(0)
        class_name = self_obj.__class__.__name__
        path_pattern = '/tmp/cache_in_tmp_{0}*.*'.format(class_name)
        for path in Files.find(path_pattern):
            print('[clear_cache_in_tmp_files] deleting file: {0}'.format(path))
            os.remove(path)
        return function(*args)
    return wrapper