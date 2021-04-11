"""Diff Entry point."""

import gendiff.differ.data_loader as data_loader
import gendiff.differ.diff_tree_generator as diff_tree_generator
import gendiff.formater.pool as formaters_pool
import gendiff.formater.stylish as stylish_formater

DEFAULT_FORMATER = stylish_formater.SELF_NAME


def generate_diff(
    first_file: str,
    second_file: str,
    format_type: str = DEFAULT_FORMATER,
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
    format_diff = formaters_pool.get(format_type)
    diff_result = diff_tree_generator.compare_data(source, compare)
    return format_diff(diff_result)
