"""Provide different funtcions for all formaters."""

from typing import Any, Union


def get_item(source: dict, path: list) -> Union[str, int, None, dict, bool]:
    """Retrives nested value recursevelly of a dict with path provided.

    Args:
        source (dict): Source dict
        path (list): Path list

    Returns:
        Union[str, int, None, dict, bool]: [description]
    """
    if not isinstance(source, dict) or not path:
        return source
    return get_item(source.get(path[0]), path[1:])


def to_string(subject: Union[str, int, bool, None, float]):
    """Convert value to string.

    Args:
        subject (Union[str, int, bool, None, float]): Subject to convert

    Returns:
        str: Converted string representation.
    """
    if isinstance(subject, bool):
        return str(subject).lower()
    elif subject == None:  # noqa:E711
        return 'null'
    return str(subject)


def get_prop_name(names: list) -> str:
    """Generate property name based on the prop path.

    Args:
        names (list): Property path

    Returns:
        str: Formated value
    """
    return '.'.join(names)


def to_simple(subject: Any) -> str:
    """Transofm object to a string.

    Args:
        subject (Any): Object to manupulate

    Returns:
        str: Formated object
    """
    if not isinstance(subject, dict):
        if isinstance(subject, str):
            return "'{0}'".format(subject)
        return to_string(subject)
    return '[complex value]'
