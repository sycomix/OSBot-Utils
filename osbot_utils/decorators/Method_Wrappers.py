import inspect
from functools import wraps

# todo: create signature based on request params so that we don't cache when the params are different
from osbot_utils.utils.Misc import get_missing_fields


def cache(function):
    """
    Use this decorator when wanting to cache a value for all executions of the current process
    """
    @wraps(function)
    def wrapper(*args,**kwargs):
        cache_id= f'osbot_cache_return_value__{function.__name__}'
        if hasattr(function, cache_id) is False:                     # check if return_value has been set
            setattr(function, cache_id,  function(*args,**kwargs))   # invoke function and capture the return value
        return getattr(function, cache_id)                           # return the return value
    return wrapper

def cache_on_self(function):
    """
    Use this for cases where we want the cache to be tied to the Class instance (i.e. not global for all executions)
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        if len(args) == 0 or inspect.isclass(type(args[0])) is False:
            raise Exception("In Method_Wrappers.cache_on_self could not find self")

        self = args[0]                                              # get self
        cache_id = f'osbot_cache_return_value__{function.__name__}' # generate cache_id
        if hasattr(self, cache_id) is False:                        # check if return_value has been set
            setattr(self, cache_id, function(*args, **kwargs))      # invoke function and capture the return value
        return getattr(self, cache_id)                              # return the return value
    return wrapper

def catch(function):
    """Catches any errors and returns an object with the error"""
    @wraps(function)                                                    # so that when we call the __name__ of the called we get the correct name (for example self.aws_lambda.alias.__name__)
    def wrapper(*args,**kwargs):
        try:
            return function(*args,**kwargs)
        except Exception as error:
            return {'error': error }
    return wrapper

class required_fields:
    """checks that required fields are not null in the current object (does not work for for static methods)"""
    def __init__(self, field_names):
        self.field_names = field_names

    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            target_obj = args[0]                                                        # self of the caller
            missing_fields = get_missing_fields(target_obj, self.field_names)
            if len(missing_fields) > 0:
                raise  Exception(f'missing fields in {function.__name__}: {missing_fields}')
            return function(*args,**kwargs)
        return wrapper

class remove:
    """removes the field from the return value of the function (if it exists"""
    def __init__(self, field_name):
        self.field_name = field_name                                # field to remove

    def __call__(self, function):
        @wraps(function)                                            # makes __name__ work ok
        def wrapper(*args,**kwargs):                                # wrapper function
            data = function(*args,**kwargs)                         # calls wrapped function with original params
            if data and data.get(self.field_name) is not None:      # check if field_name exists in data
                del data[self.field_name]                           # if it does, delete it
            return data                                             # return data received
        return wrapper                                              # return wrapper function

