"""Diff Entry point."""

import gendiff.module.data_loader as data_loader
import gendiff.module.formater.decorator as formater_decorator
import gendiff.module.walker as walker


def generate_diff(first_file, second_file, format_type: str = 'default') -> str:
    """
    Return difference in between two json files.

    Args:
        first_file (str): File path.
        second_file (str): File path.
        format_type (str): output format.

    Returns:
        str: Difference in string representation.
    """
    source = data_loader.load(first_file)
    compare = data_loader.load(second_file)

    @formater_decorator.format_difference(format_type)
    def differ(data1, data2):
        return walker.walk(data1, data2)

    return differ(source, compare)
