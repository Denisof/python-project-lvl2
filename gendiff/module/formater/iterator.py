"""Iterate over sequence."""

from typing import Callable


def get_iterator(value_processor: Callable) -> Callable:
    """Return function which apply callable to every value.

    Args:
        value_processor (Callable): Callable value receiver

    Returns:
        Callable: Function
    """
    def iter_(current_value, path):
        lines = []
        for key, key_val in current_value.items():
            lines.extend(value_processor(key_val, path + [key], iter_))
        return lines
    return iter_
