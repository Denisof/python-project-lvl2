"""Compare two structures."""


NODE_ATTRIBUTE_CHILDREN = 'children'
NODE_ATTRIBUTE_KEY = 'key'
NODE_ATTRIBUTE_VALUE = 'value'
STATUS_COLUMN = 'status'
STATUS_ADDED = 'added'
STATUS_REMOVED = 'removed'
STATUS_CHANGED = 'changed'
STATUS_UNCHANGED = 'unchanged'
VALUE_WAS = 'value_was'
VALUE_IS = 'value_is'


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
        children.append(diff)
        if key not in source:
            diff[NODE_ATTRIBUTE_VALUE] = {
                STATUS_COLUMN: STATUS_ADDED,
                VALUE_IS: compare[key],
            }
            continue
        if key not in compare:
            diff[NODE_ATTRIBUTE_VALUE] = {
                STATUS_COLUMN: STATUS_REMOVED,
                VALUE_WAS: source[key],
            }
            continue
        origin_value = source[key]
        compare_value = compare[key]
        if origin_value == compare_value:
            diff[NODE_ATTRIBUTE_VALUE] = {
                STATUS_COLUMN: STATUS_UNCHANGED,
                VALUE_IS: origin_value,
            }
            continue
        if isinstance(origin_value, dict) and isinstance(compare_value, dict):
            diff[NODE_ATTRIBUTE_CHILDREN] = compare_data(
                source[key], compare[key],
            )
            continue

        diff[NODE_ATTRIBUTE_VALUE] = {
            STATUS_COLUMN: STATUS_CHANGED,
            VALUE_WAS: origin_value,
            VALUE_IS: compare_value,
        }
    return children
