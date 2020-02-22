from unittest               import TestCase
from unittest.mock          import patch, call
from osbot_utils.utils.Dev  import Dev

class Test_Dev(TestCase):

    # Capture_Print is not needed any more since unittest.mock path decorator is a much better solution
    # def test_pprint(self): 
    #     with Capture_Print():
    #         assert Dev.pprint('aaa')     == 'aaa'
    #         assert Dev.pprint('aaa',123) == ('aaa',123)
    #     assert Capture_Print.captured_values == [{'args': (), 'options': {}}, {'args': (), 'options': {}}]

    @patch('builtins.print')
    def test_pprint__confirm_call_to_builtins_print(self, builtins_print):
        Dev.pprint('aaa')                                       # first call
        Dev.pprint('aaa',123)                                   # 2nd call
        assert builtins_print.call_count == 2                   # confirm two calls where made
        builtins_print.assert_called_with()                     # confirm last call was made with no params
        builtins_print.assert_has_calls([call(),call()])        # confirm values of two calls








    @patch('pprint.pprint')
    @patch('builtins.print')
    def atest_pprint_2(self, builtins_print,pprint_pprint):
        Dev.pprint('aaa', 123)
        builtins_print.assert_called_once_with()
        pprint_pprint.assert_called_with(123, indent=2)
        pprint_pprint.assert_has_calls([call('aaa',indent=2),call(123,indent=2)])



