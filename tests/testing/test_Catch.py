from pprint import pprint
from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.testing.Catch import Catch


class test_Catch(TestCase):

    @patch('builtins.print')
    def test_Catch(self, builtins_print):

        with Catch() as catch:
            raise Exception('new exception')
        assert builtins_print.call_count == 5

        calls = builtins_print.mock_calls
        assert calls[0] == call('')
        assert calls[1] == call('********* Catch ***********')
        assert calls[2] == call(Exception)
        assert calls[3] == call('')
        assert str(calls[4]) == str(call(Exception('new exception')))

