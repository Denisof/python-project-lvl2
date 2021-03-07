"""Format differce between two data structures as json result."""

import json


def format_diff(source: dict, compare: dict, diff_result: dict):
    """
    Make json string representation of difference result.

    Args:
        source (dict): Dict which is compared.
        compare (dict): Dict which is compared with.
        diff_result (dict): File path.

    Returns:
        string: Converted to sting difference result.
    """
    return json.dumps(diff_result, indent=4)
