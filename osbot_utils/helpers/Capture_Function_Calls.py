import builtins

class Capture_Function_Calls:
    original_function    = None                                                     # store a pointer to the original print function
    captured_values      = None                                                     # static variable to capture the values printed
    call_original        = None                                                     # option to also print the values using builtin print

    def __init__(self, target_function,call_original=False):
        Capture_Function_Calls.original_function = target_function
        Capture_Function_Calls.captured_values   = []                                        # reset static values
        Capture_Function_Calls.call_original     = call_original

    @staticmethod
    def capture(*args, **options):                                                           # method that will replace original
        Capture_Function_Calls.captured_values.append({'args': args , 'options': options})   # capture the values submitted
        if Capture_Function_Calls.call_original:                                             # if asked to also call the original function
            return Capture_Function_Calls.original_function(*args, **options)                # call it


    def hook(self):
        Capture_Function_Calls.original_function = self.capture                              # replace builtin print function with ours

    def restore(self):
        builtins.print = self.builtin_print                                         # restore original builtin print function

    def __enter__(self):                                                            # in the beginning of the 'with block'
        self.hook_print()                                                           #   hook print function
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):                                  # at the end of the 'with block'
        self.restore_print()                                                        #   restore print function

