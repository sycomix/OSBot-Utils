class Fluent_List(list):
    def __new__(cls, *args, **kwargs):
        first_one = args[0]
        return super().__new__(cls, first_one)

    def __init__(self,*args,**kwargs):
        self.data = args[0]
        super().__init__(*args,**kwargs)

    def sorted(self):
        return sorted(self.data)

    def type(self):                         # todo: find a way to add this kind of methods to all Fluent Classes
        return type(self)