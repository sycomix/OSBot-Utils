from pprint import pprint
from unittest import TestCase
from unittest.mock import patch, call

import pytest
from   osbot_utils.utils.Dev import Dev

from osbot_utils.testing.Unit_Test import Unit_Test


class test_Unit_Test(TestCase):

    def setUp(self) -> None:
        self.unit_test = Unit_Test()
        self.unit_test.setUp()

    def test_setUp(self):

        assert self.unit_test.png_file == '/tmp/unit-test.png'
        assert self.unit_test.result   is None
        assert self.unit_test.png_data is None

    @pytest.mark.skip("Needs fixing pprint is not being patched any more")
    @patch('osbot_utils.utils.Dev.pprint')
    def test_tearDown(self, dev_pprint):
        self.unit_test.tearDown()
        assert dev_pprint.mock_calls == []
        self.unit_test.result = "an result"
        self.unit_test.tearDown()
        assert dev_pprint.mock_calls == [call.pprint('an result', indent=2)]
        dev_pprint.reset_mock()

        self.unit_test.result = None
        self.unit_test.png_data = "an string"
        self.unit_test.tearDown()
        assert dev_pprint.mock_calls == [call.pprint('Png data with size 9 saved to /tmp/unit-test.png', indent=2)]
        dev_pprint.reset_mock()

        self.unit_test.png_data = "an string".encode()
        self.unit_test.tearDown()
        #[call.pprint('an result', indent=2), call.pprint('an result', indent=2)]
        assert dev_pprint.mock_calls == [call.pprint('Png data with size 9 saved to /tmp/unit-test.png', indent=2)]
        dev_pprint.reset_mock()

        self.unit_test.png_data = {}
        self.unit_test.tearDown()
        assert dev_pprint.mock_calls == [call.pprint('Error Png data was not a string: {}', indent=2)]
        dev_pprint.reset_mock()

        self.unit_test.png_data = "__OonJ69bl_#U;]S5b1f@q"
        self.unit_test.tearDown()
        assert dev_pprint.mock_calls == [call.pprint('png save error: Incorrect padding', indent=2), call.pprint('__OonJ69bl_#U;]S5b1f@q', indent=2)]
