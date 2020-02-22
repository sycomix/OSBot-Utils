from unittest import TestCase

from osbot_utils.helpers.Capture_Print import Capture_Print


class test_Capture_Print(TestCase):

    def test_with_block(self):
        with Capture_Print():
            assert Capture_Print.print_using_builtin is False
            assert Capture_Print.captured_values     == []
            print('1st time')
            assert Capture_Print.captured_values     == [{'args': ('1st time',), 'options': {}}]

        with Capture_Print():
            assert Capture_Print.print_using_builtin is False
            assert Capture_Print.captured_values     == []
            print('2nd time', end='\nABC\n')
            assert Capture_Print.captured_values     == [{'args': ('2nd time',), 'options': {'end' : '\nABC\n'}}]

        with Capture_Print(True):
            text = 'this will show on the console'
            assert Capture_Print.print_using_builtin is True
            print(text)
            assert Capture_Print.captured_values     == [{'args': (text,), 'options': {}}]

