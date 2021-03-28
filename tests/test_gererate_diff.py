# -*- coding:utf-8 -*-

"""Generate diff tests."""
import os

import pytest

from gendiff.differ.processor import generate_diff


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "fixtures", file_name)


def read(file_path):
    with open(file_path, "r") as fl:
        result = fl.read()
    return result


cases = [
    (
        get_fixture_path("flat_1.json"),
        get_fixture_path("flat_2.json"),
        "stylish",
        read(get_fixture_path("stylish_result/flat_json.txt")),
    ),
    (
        get_fixture_path("flat_1.yml"),
        get_fixture_path("flat_2.yml"),
        "stylish",
        read(get_fixture_path("stylish_result/flat_yaml.txt")),
    ),
    (
        get_fixture_path("nested_1.json"),
        get_fixture_path("nested_2.json"),
        "stylish",
        read(get_fixture_path("stylish_result/nested_json.txt")),
    ),
    (
        get_fixture_path("nested_1.json"),
        get_fixture_path("nested_2.json"),
        "plain",
        read(get_fixture_path("plain_result/nested_json.txt")),
    ),
    (
        get_fixture_path("nested_1.json"),
        get_fixture_path("nested_2.json"),
        "json",
        read(get_fixture_path("json_result/nested_json.txt")),
    ),
    (
        get_fixture_path("nested_1.yml"),
        get_fixture_path("nested_2.yml"),
        "stylish",
        read(get_fixture_path("stylish_result/nested_yml.txt")),
    ),
]


@pytest.mark.parametrize("file_1,file_2,format,expected", cases)
def test_diff_generation(file_1, file_2, format, expected):
    assert generate_diff(file_1, file_2, format) == expected


def test_wrong_extension():
    with pytest.raises(ValueError) as excinfo:
        generate_diff(
            get_fixture_path("flat_1.txt"), get_fixture_path("flat_1.json")
        )
    assert "Wrong file extension" in str(excinfo.value)
