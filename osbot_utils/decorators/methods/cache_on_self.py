import inspect
from functools import wraps


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