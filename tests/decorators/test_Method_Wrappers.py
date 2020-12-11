from unittest import TestCase

import pytest

skip = pytest.mark.skip

class test_Method_Wrappers(TestCase):

    @skip("todo")   # todo: create test to double check behaviour of decorator
    def test_cache(self):
        pass

    @skip("catch")  # todo: create test to double check behaviour of decorator
    def test_cache(self):
        pass

    @skip("required_fields")  # todo: create test to double check behaviour of decorator
    def test_cache(self):
        pass

    @skip("remove")  # todo: create test to double check behaviour of decorator
    def test_cache(self):
        pass
