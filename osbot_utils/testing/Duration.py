from pprint import pprint

from osbot_utils.utils.Misc import date_time_now, time_delta_to_str


class Duration:
    """
    Helper class for to capture time duration
    """
    def __init__(self, use_utc=True, print_result=True):
        self.use_utc            = use_utc
        self.print_result       = print_result
        self.start              = None
        self.end                = None
        self.duration           = None

    def __enter__(self):
        self.start = date_time_now(use_utc=self.use_utc, return_str=False)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.end      = date_time_now(use_utc=self.use_utc, return_str=False)
        self.duration = self.end - self.start
        if self.print_result:
            print(f"\nDuration: {time_delta_to_str(self.duration)}\n")

    def seconds(self):
        return self.duration.total_seconds()