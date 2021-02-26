"""Format differce between two data structures."""

import itertools



def format(source: dict, compare: dict, diff_result: dict):
    replacer = ' '
    spaces_count = 4
    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return str(current_value)

        deep_indent_size = depth + spaces_count
        deep_indent = replacer * deep_indent_size
        current_indent = replacer * depth
        lines = []
        for key, val in current_value.items():
            foramted_val = iter_(val, deep_indent_size)
            lines.append(f'{deep_indent}{key}: {foramted_val}')
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(source, 0)
