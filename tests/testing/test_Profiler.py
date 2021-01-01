import sys
from pprint import pprint
from unittest import TestCase

from py._code.code import Frame

from osbot_utils.testing.Profiler import Profiler
from osbot_utils.utils.Misc import under_debugger


class An_Class:
    def an_function(self):
        local_var = 42
        return local_var

class test_Profiler(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test___enter___exit(self):
        profiler = Profiler()
        profiler.__enter__().__exit__(None, None, None)
        assert len(profiler.events) == 0

    def test_current_profiler(self):
        with Profiler() as trace:
            assert An_Class().an_function() == 42
            assert trace.current_profiler() == trace.profiler

        assert trace.current_profiler() is trace.previous_profiler
        assert len(trace.events)      == 2
        assert trace.events.pop()['f_locals']['local_var'] == 42

    def test_profiler(self):
        frame = sys._getframe(0)  # get current frame
        event = {}
        arg = {}

        profiler = Profiler()
        profiler.profiler(frame, event, arg)
        assert len(profiler.events) == 1