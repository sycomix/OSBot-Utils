def obj_all_base_classes(obj):
    return type_all_base_classes(type(obj))

def type_all_base_classes(cls):
    base_classes = cls.__bases__
    all_base_classes = list(base_classes)
    for base in base_classes:
        all_base_classes.extend(type_all_base_classes(base))
    return all_base_classes