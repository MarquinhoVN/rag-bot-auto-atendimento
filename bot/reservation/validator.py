def is_empty(value):
    return value in [None, ""]

def is_valid_quantity(value):
    return isinstance(value, int) and 1 <= value <= 10