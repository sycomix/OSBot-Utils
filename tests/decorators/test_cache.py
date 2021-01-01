from pprint import pprint
from unittest import TestCase

from osbot_utils.decorators.methods.cache import cache
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.testing.Catch import Catch


class test_cache(TestCase):

    def test_cache(self):

        class An_Class:
            @cache
            def an_function(self):
                return 42

        an_class    = An_Class()

        assert an_class.an_function() == 42

        function = None

        def tracer(frame, event, arg):
            #print('***', event, set(frame.f_locals))
            if event == 'return':
                function = frame.f_locals['function']
                print(dir(function))
                print(event, set(frame.f_locals))
                print(function.osbot_cache_return_value__an_function)
                function.osbot_cache_return_value__an_function = 123
                #_locals = frame.f_locals.copy()

        # tracer is activated on next call, return or exception
        print()
        import sys
        sys.setprofile(tracer)
        try:
            # trace the function call
            an_class.an_function()
        finally:
            sys.setprofile(None) # disable tracer

        print(an_class.an_function()) # osbot_cache_return_value__an_function

        #an_class.an_function()
        #assert an_class.an_function.osbot_cache_return_value__an_function == 42
        #an_class.an_function.osbot_cache_return_value__an_function = 12
        #assert an_class.an_function.osbot_cache_return_value__an_function == 12

    def test_cache_on_self__outside_an_class(self):

        @cache_on_self
        def an_function():
            pass

        with Catch(log_exception=False) as catch:
            an_function()

        assert catch.exception_value.args[0] == "In Method_Wrappers.cache_on_self could not find self"