class Lists:

    @staticmethod
    def chunks(list, split_by):
        n = max(1, split_by)
        return (list[i:i + n] for i in range(0, len(list), n))

    @staticmethod
    def first(list, strip=False):
        if Lists.not_empty(list):
            value = list[0]
            if strip:
                value = value.strip()
            return value

    @staticmethod
    def not_empty(list):
        if list and type(list).__name__ == 'list' and len(list) >0:
            return True
        return False

    @staticmethod
    def empty(list):
        return not Lists.not_empty(list)

    def tuple_to_list(target:tuple):
            if type(target) is tuple:
                return list(target)

    def tuple_replace_position(target:tuple, position,value):
        tuple_as_list = tuple_to_list(target)
        if len(tuple_as_list) > position:
            tuple_as_list[position] = value
        list_as_tuple = list_to_tuple(tuple_as_list)
        return list_as_tuple

    def list_to_tuple(target: list):
        if type(target) is list:
            return tuple(target)

list_chunks            = Lists.chunks
list_empty             = Lists.empty
list_first             = Lists.first
list_not_empty         = Lists.not_empty
list_to_tuple          = Lists.list_to_tuple

tuple_to_list          = Lists.tuple_to_list
tuple_replace_position = Lists.tuple_replace_position
