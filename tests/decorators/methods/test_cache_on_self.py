from pprint import pprint
from unittest import TestCase

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.testing.Catch import Catch


class test_cache_on_self(TestCase):

    def test_cache_on_self(self):

        class An_Class:
            @cache_on_self
            def an_function(self):
                return 42

        an_class    = An_Class()
        assert an_class.an_function() == 42
        assert an_class.osbot_cache_return_value__an_function == 42
        an_class.osbot_cache_return_value__an_function = 12
        assert an_class.osbot_cache_return_value__an_function == 12

    def test_cache_on_self__outside_an_class(self):

        @cache_on_self
        def an_function():
            pass

        with Catch(log_exception=False) as catch:
            an_function()

        assert catch.exception_value.args[0] == "In Method_Wrappers.cache_on_self could not find self"