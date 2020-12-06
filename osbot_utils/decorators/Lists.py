from functools import wraps
from osbot_utils.fluent.Fluent_Dict import Fluent_Dict


# todo: find way to also allow the used of function().index_by(key) to working
#     : maybe using Fluent_List
def index_by(function):                                 # returns the list provided indexed by the key provided in index_by
    def apply(key, values):
        if key:
            results = {}
            for item in values:
                results[item.get(key)] = item
            return Fluent_Dict(results)
        return values

    @wraps(function)
    def wrapper(*args,**kwargs):
        key = None
        if 'index_by' in kwargs:
            key = kwargs.get('index_by')
            del kwargs['index_by']
        values = function(*args,**kwargs)

        return apply(key,values)
    return wrapper

#todo: refactor with index_by
def group_by(function):                                 # returns the list provided grouped by the key provided in group_by
    @wraps(function)
    def wrapper(*args,**kwargs):
        key = None
        if 'group_by' in kwargs:
            key = kwargs.get('group_by')
            del kwargs['group_by']
        values = function(*args,**kwargs)
        if key:
            results = {}
            for item in values:
                value = item.get(key)
                if results.get(value) is None: results[value] = []
                results[value].append(item)
            return results
        return values
    return wrapper