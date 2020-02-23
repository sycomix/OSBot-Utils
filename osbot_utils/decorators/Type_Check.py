from functools import wraps

# this is an attempt at creating something simpler than
#  - https://github.com/agronholm/typeguard
#  - https://github.com/Stewori/pytypes


def function_type_check(function):

    @wraps(function)
    def wrapper(*args,**kwargs):
        _args       = list(args)
        annotations = function.__annotations__
        for name, var_type in annotations.items():
            if name=='return': continue
            if _args:
                value = _args.pop(0)
            else:
                value = kwargs.get(name)
            if value is not None:
                #if isinstance(value, var_type) is False:                           # false positive with int and bool
                if type(value) is not var_type:
                    raise Exception(f'in function "{function.__name__}", the provided param "{value}" was an "{type(value)}" and it was expected to be {var_type}')
        return_value = function(*args, **kwargs)
        return_type  = annotations.get('return')
        if annotations.get('return'):
            if type(return_value) is not return_type:
                raise Exception(f'in function "{function.__name__}", the provided return value "{return_value}" was an "{type(return_value)}" and it was expected to be {return_type}')
        return return_value

    return wrapper

def class_type_check(Target_Class):                                   #
    class Wrapped_Cls(object):
        def __init__(self,*args,**kwargs):
            self.target_class = Target_Class(*args,**kwargs)          #

        def __getattribute__(self,s):
            try:
                x = super(Wrapped_Cls,self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.target_class.__getattribute__(s)
            if type(x) == type(self.__init__):                # it is an instance method
                return function_type_check(x)                 # this is equivalent of just decorating the method with function_type_check
            else:
                return x

    return Wrapped_Cls