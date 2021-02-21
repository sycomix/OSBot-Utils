# todo: refactor into separate project (since the idea is to minimize the dependencies on OSBot-Utils
#       maybe on a lambda function (which will have the required dependencies)


# todo: see if we can use the python native trace and code coverage to create something similar
#       if this mode creates a graph, then an external service (or lambda function) could be used to
#       create the actual image

# import trace
# import sys
#
# pprint(sys.prefix)
# ignore_dirs = list_contains(sys.path, 'python3.8')
# # return
# tracer = trace.Trace(
#     ignoredirs=ignore_dirs,
#     # ignoremods=['inspect','enum', '__init__'],
#     countfuncs=1,
#     countcallers=1,
#     trace=1,
#     count=1,
#     timing=True)
# result = tracer.runfunc(self.session.credentials_ok)
#
# # pprint(result)
# # results = tracer.results()
# pprint(dir(tracer))
# print(results.write_results(show_missing=True, coverdir="."))
# pprint(results.calledfuncs)
# pprint(results.callers)
# pprint(results.counts)

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
