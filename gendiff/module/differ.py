"""Diff Entry point."""
import json
from itertools import chain

def generate_diff(first_file, second_file):
    dict_1 = json.load(open(first_file))
    dict_2 = json.load(open(second_file))
    result = []
    for key in sorted(dict_1.keys() | dict_2.keys()):
        if key not in dict_1:
            result.append(f' + {key}: {dict_2[key]}')
        elif key not in dict_2:
            result.append(f' - {key}: {dict_1[key]}')
        elif dict_1[key] == dict_2[key]:
            result.append(f'   {key}: {dict_1[key]}')
        else:
            result.append(f' - {key}: {dict_1[key]}')
            result.append(f' + {key}: {dict_2[key]}')
    result = chain("{", result, "}")
    return '\n'.join(result)