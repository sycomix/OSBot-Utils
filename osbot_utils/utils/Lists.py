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

list_chunks    = Lists.chunks
list_empty     = Lists.empty
list_first     = Lists.first
list_not_empty = Lists.not_empty
