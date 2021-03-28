"""Compare two structures."""


from typing import Optional

FLAG_UNCHANGED = ' '
FLAG_ADDED = '+'
FLAG_REMOVED = '-'
NODE_ATTRIBUTE_CHILDREN = 'children'
NODE_ATTRIBUTE_KEY = 'key'
NODE_ATTRIBUTE_VALUE = 'value'


def compare_data(source: dict, compare: dict) -> dict:
    """Compare two structures recursevelly.

    Args:
        source (dict): Source data
        compare (dict): Data to compare

    Returns:
        dict: Result of camparasion
    """
    children = []
    for key in sorted(source.keys() | compare.keys()):
        diff = {}
        diff[NODE_ATTRIBUTE_KEY] = key
        diff_result = get_prop_transition(key, source, compare)
        if diff_result:
            diff[NODE_ATTRIBUTE_VALUE] = diff_result
        else:
            diff[NODE_ATTRIBUTE_CHILDREN] = compare_data(
                source[key], compare[key],
            )
        children.append(diff)

    return children


def get_prop_transition(
    key: str, source: dict, compare: dict,
) -> Optional[dict]:
    """Calculate property trasnition.

    Args:
        key (str): property key
        source (dict): Source dict
        compare (dict): Dict to compare

    Returns:
        Optional[dict]: Result
    """
    if key not in source:
        return {FLAG_ADDED: compare[key]}
    elif key not in compare:
        return {FLAG_REMOVED: source[key]}
    origin_value = source[key]
    compare_value = compare[key]
    if origin_value == compare_value:
        return {FLAG_UNCHANGED: origin_value}
    elif isinstance(origin_value, dict) and isinstance(compare_value, dict):
        return None
    return {FLAG_REMOVED: origin_value, FLAG_ADDED: compare_value}
