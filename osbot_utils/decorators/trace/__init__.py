from functools import wraps

from osbot_utils.decorators.trace.Trace_Call import Trace_Call


def trace(function):
    @wraps(function)
    def wrapper(*args,**kwargs):
        trace_call = Trace_Call()
        trace_call.include_filter = ['botocore.http*']#'osbot*', 'gwbot*', 'boto*', 'ConnectionPool*']
        return trace_call.invoke_method(function, *args,**kwargs)

        # print('\n aaaaaa  -- before')
        # result = function(*args,**kwargs)
        # print(f'\n aaaaaa  -- after: {result}')
        # return result
    return wrapper

