"""Compare two structures."""


from typing import Optional

import gendiff.module.flag as flag


def walk(source: dict, compare: dict) -> dict:
    """Compare two structures recursevelly.

    Args:
        source (dict): Source data
        compare (dict): Data to compare

    Returns:
        dict: Result of camparasion
    """
    diff = {}
    for key in sorted(source.keys() | compare.keys()):
        diff_result = get_prop_transition(key, source, compare)
        if not diff_result:
            diff_result = walk(source[key], compare[key])
        diff[key] = diff_result
    return diff


def get_prop_transition(key: str, source: dict, compare: dict) -> Optional[str]:
    """Calculate property trasnition.

    Args:
        key (str): property key
        source (dict): Source dict
        compare (dict): Dict to compare

    Returns:
        Optional[str]: Result
    """
    if key not in source:
        return flag.FLAG_ADDED
    elif key not in compare:
        return flag.FLAG_REMOVED
    elif source[key] == compare[key]:
        return flag.FLAG_UNCHANGED
    elif not all(  # noqa:WPS337
        map(
            lambda prop_val: isinstance(prop_val, dict),
            [source[key], compare[key]],
        ),
    ):
        return flag.FLAG_CHANGED
