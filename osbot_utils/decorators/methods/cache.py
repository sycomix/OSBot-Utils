from functools import wraps

# todo: create signature based on request params so that we don't cache when the params are different

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