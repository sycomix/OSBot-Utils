import inspect
from functools import wraps
from osbot_utils.utils.Misc import date_time_now, time_delta_to_str


def duration(func):
    if inspect.iscoroutinefunction(func):
        # It's an async function
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with Duration(prefix=f'.{func.__name__} took'):
                return await func(*args, **kwargs)
        return async_wrapper
    else:
        # It's a regular function
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with Duration(prefix=f'.{func.__name__} took'):
                return func(*args, **kwargs)
        return sync_wrapper

class Duration:
    """
    Helper class for to capture time duration
    """
    def __init__(self, print_result=True, use_utc=True, prefix="\nDuration:"):
        self.use_utc            = use_utc
        self.print_result       = print_result
        self.prefix             = prefix
        self.start_time         = None
        self.end_time           = None
        self.duration           = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.end()

    def start(self):
        self.start_time = date_time_now(use_utc=self.use_utc, return_str=False)

    def end(self):
        self.end_time = date_time_now(use_utc=self.use_utc, return_str=False)
        self.duration = self.end_time - self.start_time
        if self.print_result:
            print(f"{self.prefix} {time_delta_to_str(self.duration)}")

    def seconds(self):
        return self.duration.total_seconds()