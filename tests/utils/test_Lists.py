from unittest import TestCase

from osbot_utils.utils.Lists import list_empty, list_first, list_not_empty


class test_Lists(TestCase):

    def test_list_empty(self):
        assert list_empty([]   ) is True
        assert list_empty(['a']) is False

    def test_list_first(self):
        assert list_first(['a ','b']             ) is 'a '
        assert list_first(['a', 'b'], strip=True) is 'a'
        assert list_first([]) is None

    def test_list_not_empty(self):
        assert list_not_empty([]   ) is False
        assert list_not_empty(['a']) is True