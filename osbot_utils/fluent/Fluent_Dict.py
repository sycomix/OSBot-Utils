from osbot_utils.fluent.Fluent_List import Fluent_List


class Fluent_Dict(dict):
    def __new__(cls, *args, **kwargs):
        first_one = args[0]
        return super().__new__(cls, first_one)

    def __init__(self,*args,**kwargs):
        self.data = args[0]
        super().__init__(*args,**kwargs)

    def size(self):
        return len(self.data)

    def keys(self):
        return Fluent_List(list(self.data.keys()))

    def type(self):
        return type(self)