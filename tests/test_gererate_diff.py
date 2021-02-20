# -*- coding:utf-8 -*-

"""Generate diff tests."""
import os

import pytest

from gendiff.module.differ import generate_diff

def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path):
    with open(file_path, 'r') as f:
        result = f.read()
    return result


cases = [
    (
        get_fixture_path('flat_1.json'),
        get_fixture_path('flat_2.json'),
        read(get_fixture_path('flat_result.txt')),
    )
]
@pytest.mark.parametrize("file_1,file_2,expected", cases)
def test_flat(file_1, file_2, expected):
    assert generate_diff(file_1, file_2) == expected
