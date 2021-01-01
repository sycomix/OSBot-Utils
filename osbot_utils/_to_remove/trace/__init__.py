# # todo: refactor into separate project (since the idea is to minimize the dependencies on OSBot-Utils
#   todo:   maybe on a lambda function (which will have the required dependencies)
# from functools import wraps
#
# from osbot_utils.decorators.trace.Trace_Call import Trace_Call
#
# class trace:
#
#     def __init__(self,include=None, exclude=None):
#         self.include = include
#         self.exclude = exclude
#         pass
#         #self.fields = fields                                        # field to inject
#
#     def __call__(self, function):
#         @wraps(function)
#         def wrapper(*args,**kwargs):
#             trace_call = Trace_Call(self.include, self.exclude)
#             #if self.include: trace_call.include_filter = self.include
#             #if self.exclude: trace_call.exclude_filter = self.exclude
#             #trace_call.include_filter = ['botocore.http*']#'osbot*', 'gwbot*', 'boto*', 'ConnectionPool*']
#             return trace_call.invoke_method(function, *args,**kwargs)
#         return wrapper
#
#
