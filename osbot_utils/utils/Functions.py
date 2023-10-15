import inspect
import textwrap
import types


def function_source_code(function):
    if isinstance(function, types.FunctionType):
        source_code = inspect.getsource(function)
        source_code = textwrap.dedent(source_code).strip()
        return source_code
    elif isinstance(function, str):
        return function
    return None