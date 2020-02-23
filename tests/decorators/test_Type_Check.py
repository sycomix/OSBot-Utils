from unittest import TestCase

from osbot_utils.decorators.Type_Check import class_type_check, function_type_check


@class_type_check
class An_Class:

    def method_1(self, an_int: int, an_string: str, an_bool : bool = False ) -> int:
        print('---- in method 1')
        return 12

    def method_2(self):
        print('---- in method 2')

    def method_3(self,return_me) -> str:
        return return_me

    @staticmethod
    def method_4(an_int : int, an_string:str) -> int:
        return an_int

class test_Type_Check(TestCase):

    def setUp(self) -> None:
        pass

    def test_function_type_checker(self):
        def an_method(an_string: str, an_int:int=0, an_bool:bool=False):
            pass

        wrapped_function = function_type_check(an_method)

        wrapped_function('abca')
        wrapped_function('abca', 42)
        wrapped_function('abca', an_bool=False)

        self.assertRaises(Exception, wrapped_function, 12         )
        self.assertRaises(Exception, wrapped_function, 'a','a'    )
        self.assertRaises(Exception, wrapped_function, 'a', False )
        self.assertRaises(Exception, wrapped_function, 'a', 12,'a')



    def test_class_decorator(self):
        an_class = An_Class()
        an_class.method_1(12,'b')
        an_class.method_1(12,'b')
        an_class.method_1(12,'b',False)
        an_class.method_2()
        an_class.method_3('a')

        self.assertRaises(Exception, an_class.method_1, 12         )
        self.assertRaises(Exception, an_class.method_1, 12, 12     )
        self.assertRaises(Exception, an_class.method_1, 12, False  )
        self.assertRaises(Exception, an_class.method_1, 12, 'a','a')
        self.assertRaises(Exception, an_class.method_2, 'a'        )
        self.assertRaises(Exception, an_class.method_3, 12         )
        self.assertRaises(Exception, an_class.method_3, False      )
        self.assertRaises(Exception, an_class.method_3, None       )

    def test_class_decorator_static_method(self):
        an_class = An_Class()
        import inspect
        from optparse import OptionParser

        members = inspect.getmembers(an_class, predicate=inspect.ismethod)
        from osbot_utils.utils.Dev import Dev
        Dev.pprint(members)
        #an_class.method_4()