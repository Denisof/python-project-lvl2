"""Format differce between two data structures as json result."""

import json

SELF_NAME = 'json'


def format_diff(diff_result: dict):
    """
    Make json string representation of difference result.

    Args:
        diff_result (dict): File path.

    Returns:
        string: Converted to sting difference result.
    """
    return json.dumps(diff_result, indent=4)
