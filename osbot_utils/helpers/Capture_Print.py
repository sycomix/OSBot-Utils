import builtins

class Capture_Print:
    builtin_print = builtins.print                                                  # store a pointer to the original print function
    captured_values      = None                                                     # static variable to capture the values printed
    print_using_builtin  = None                                                     # option to also print the values using builtin print

    def __init__(self, print_using_builtin=False):
        Capture_Print.captured_values = []                                          # reset static values
        Capture_Print.print_using_builtin = print_using_builtin

    @staticmethod
    def print(*args, **options):                                                    # new print method
        if Capture_Print.print_using_builtin:                                       # if print_using_builtin is set
            Capture_Print.builtin_print(*args, **options)                           #    then use the buildin print to print it
        Capture_Print.captured_values.append({'args': args , 'options': options})   # capture the values submitted

    def hook_print(self):
        builtins.print = self.print                                                 # replace builtin print function with ours

    def restore_print(self):
        builtins.print = self.builtin_print                                         # restore original builtin print function

    def __enter__(self):                                                            # in the beginning of the 'with block'
        self.hook_print()                                                           #   hook print function
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):                                  # at the end of the 'with block'
        self.restore_print()                                                        #   restore print function

