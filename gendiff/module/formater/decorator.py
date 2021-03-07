"""Diff Entry point."""
import functools

import gendiff.module.formater.default as default_formater
import gendiff.module.formater.json as json_formater
import gendiff.module.formater.plain as plain_formater


def format_difference(output_format: str):
    """Format diff_generate result to text form.

    Args:
        output_format (str): Format type

    Returns:
        func: Wrapper function
    """
    if output_format == 'plain':
        formater = plain_formater
    elif output_format == 'json':
        formater = json_formater
    else:
        formater = default_formater

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            diff_result = func(*args, **kwargs)
            return formater.format_diff(*args, diff_result=diff_result)
        return inner

    return wrapper
