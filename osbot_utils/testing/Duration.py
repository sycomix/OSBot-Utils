from pprint import pprint

from osbot_utils.utils.Misc import date_time_now, time_delta_to_str


class Duration:
    """
    Helper class for to capture time duration
    """
    def __init__(self, print_result=False, use_utc=True, prefix="\nDuration..."):
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