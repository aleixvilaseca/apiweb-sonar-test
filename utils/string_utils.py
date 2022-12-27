from functools import reduce

def snake_case(str):
    str = str.lower()
    str = reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, str).lower()
    str = str.replace(' ', '_')
    return str