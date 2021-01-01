from pprint import pprint


class Catch:
    """
    Helper class for cases when the native Python exception traces is too noisy
    """
    def __init__(self, log_exception=True, logger=None):
        self.log_exception       = log_exception
        self.logger              = logger or print
        self.exception_type      = None
        self.exception_value     = None
        self.exception_traceback = None
        self.execution_complete  = False

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.exception_type      = exception_type
        self.exception_value     = exception_value
        self.exception_traceback = exception_traceback
        self.execution_complete  = True
        if (self.log_exception):
            if (exception_type is not None):
                self.log()
                self.log("***************************")
                self.log("********* Catch ***********")
                self.log("***************************")
                self.log()
                self.log(exception_type)
                self.log()
                self.log(exception_value)
        return True     # returning true here will prevent the exception to be propagated (which is the objective of this class :) )

    def log(self, message=''):
        self.logger(message)