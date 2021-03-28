"""Provide decorator to format diff result."""
import functools

import gendiff.formater.json as json_formater
import gendiff.formater.plain as plain_formater
import gendiff.formater.stylish as stylish_formater


def format_difference(output_format: str):
    """Format diff_generate result to text form.

    Args:
        output_format (str): Format type

    Returns:
        func: Wrapper function
    """
    if output_format == plain_formater.SELF_NAME:
        formater = plain_formater
    elif output_format == json_formater.SELF_NAME:
        formater = json_formater
    else:
        formater = stylish_formater

    def wrapper(func):  # noqa:WPS430
        @functools.wraps(func)
        def inner(*args, **kwargs):  # noqa:WPS430
            diff_result = func(*args, **kwargs)
            return formater.format_diff(diff_result=diff_result)

        return inner

    return wrapper
