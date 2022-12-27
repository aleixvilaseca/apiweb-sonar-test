from operator import itemgetter

def convert_tuple_to_dict(tup, di):
    di = dict(tup)
    return di

def order_dict(dictionary, list_order):
    index_map = {v: i for i, v in enumerate(list_order)}
    ordered = sorted(dictionary.items(), key=lambda pair: index_map[pair[0]])
    return convert_tuple_to_dict(ordered, dict())

def reverse_dict(_dict):
    return dict(reversed(list(_dict.items())))

def copy_dict_keys_new_dict(original:dict, default_value=None):
    new = dict.fromkeys(original.keys(), default_value)
    return new

def get_n_top_values_from_dict(dictionary, n_values = 1):
    return dict(sorted(dictionary.items(), key = itemgetter(1), reverse = True)[:n_values])
