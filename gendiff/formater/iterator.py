"""Iterate over sequence."""

from typing import Generator

import gendiff.differ.diff_tree_generator as diff_tree_generator


def iter_node(childen: list, path: list) -> Generator:
    """Iterate over diff tree.

    Args:
        childen (list): [description]
        path (list): [description]. Defaults to [].

    Yields:
        Generator: [description]
    """
    for node in childen:
        cur_path = path[:]
        cur_path.append(node.get(diff_tree_generator.NODE_ATTRIBUTE_KEY))
        if not node.get(diff_tree_generator.NODE_ATTRIBUTE_CHILDREN):
            yield (cur_path, node.get(diff_tree_generator.NODE_ATTRIBUTE_VALUE))
            continue
        yield from iter_node(
            node.get(diff_tree_generator.NODE_ATTRIBUTE_CHILDREN),
            cur_path,
        )
