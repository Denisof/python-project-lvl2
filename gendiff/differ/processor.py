"""Diff Entry point."""

import gendiff.differ.data_loader as data_loader
import gendiff.differ.diff_tree_generator as diff_tree_generator
import gendiff.formater.decorator as formater_decorator
import gendiff.formater.stylish as stylish_formater


def generate_diff(
    first_file: str,
    second_file: str,
    format_type: str = stylish_formater.SELF_NAME,
) -> str:
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
    formater = formater_decorator.format_difference(format_type)
    diff_decorator = formater(diff_tree_generator.compare_data)
    return diff_decorator(source, compare)