"""Provide diff formater based on the type."""

import gendiff.formater.json as json_formater
import gendiff.formater.plain as plain_formater
import gendiff.formater.stylish as stylish_formater


def get(formater_type: str):
    """Format diff_generate result to text form.

    Args:
        formater_type (str): Format type

    Raises:
        ValueError: [description]

    Returns:
        func: Wrapper function
    """
    if formater_type == plain_formater.SELF_NAME:
        return plain_formater.format_diff
    if formater_type == json_formater.SELF_NAME:
        return json_formater.format_diff
    if formater_type == stylish_formater.SELF_NAME:
        return stylish_formater.format_diff
    raise ValueError('Unknown formater type: {0}'.format(formater_type))
