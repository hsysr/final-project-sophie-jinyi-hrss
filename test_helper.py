import pytest
from datetime import datetime


@pytest.mark.parametrize("value, types, expected", [
    ["1", [str], True],
    [1, [str], False],
    [1, [str, int], True],
    [[1, 2, 3], [str, int], False],
    [[1, 2, 3], [str, list], True]
])
def test_type_check(value, types, expected):
    from helper import type_check
    answer = type_check(value, types)
    assert answer == expected


@pytest.mark.parametrize("input_dict, validation_dict, expected", [
    [{"MRN": 5,
      "name": 'Smith.J',
      "medical_image": '',
      "heart_rate": 70,
      "ECG_image": ''},
     {"MRN": [int],
      "name": [str],
      "medical_image": [str],
      "heart_rate": [int],
      "ECG_image": [str]},
     True],
    [{"MRN": '5',
      "name": 'Smith.J',
      "medical_image": '',
      "heart_rate": 70,
      "ECG_image": ''},
     {"MRN": [int],
      "name": [str],
      "medical_image": [str],
      "heart_rate": [int],
      "ECG_image": [str]},
     False],
    [{"name": 'Smith.J',
      "medical_image": '',
      "heart_rate": 70,
      "ECG_image": ''},
     {"MRN": [int],
      "name": [str],
      "medical_image": [str],
      "heart_rate": [int],
      "ECG_image": [str]},
     False],
    [{"MRN": 5,
      "medical_image": '',
      "heart_rate": 70,
      "ECG_image": ''},
     {"MRN": [int],
      "name": [str],
      "medical_image": [str],
      "heart_rate": [int],
      "ECG_image": [str]},
     False],
    [{"MRN": 5,
      "name": 'Smith.J',
      "medical_image": 54646,
      "heart_rate": 70,
      "ECG_image": ''},
     {"MRN": [int],
      "name": [str],
      "medical_image": [str],
      "heart_rate": [int],
      "ECG_image": [str]},
     False]
])
def test_validate_input_dict(input_dict, validation_dict, expected):
    from helper import validate_input_dict
    answer = validate_input_dict(input_dict, validation_dict)
    assert answer == expected


@pytest.mark.parametrize("s, expected", [
    ["1", 1],
    ["114514", 114514],
    ["1a", None],
    [".", None],
    ["", None]
])
def test_num_parse(s, expected):
    from helper import num_parse
    answer = num_parse(s)
    assert answer == expected


@pytest.mark.parametrize("timestamp, expected", [
    [datetime(2018, 3, 9, 11, 0, 36), "2018-03-09 11:00:36"],
    [datetime(1996, 4, 15, 19, 56, 44), "1996-04-15 19:56:44"]
])
def test_timestamp_format(timestamp, expected):
    from helper import timestamp_format
    answer = timestamp_format(timestamp)
    assert answer == expected


@pytest.mark.parametrize("filename, expected", [
    ['images/acl1.jpg', '/9j/4AAQSkZJRgABAgAA'],
    ['images/acl2.jpg', '/9j/4AAQSkZJRgABAgAA'],
    ['images/blank-avatar.jpg', 'iVBORw0KGgoAAAANSUhE'],
    ['images/synpic50411.jpg', '/9j/4AAQSkZJRgABAgAA']
])
def test_file_to_b64_string(filename, expected):
    from helper import file_to_b64_string
    answer = file_to_b64_string(filename)
    assert answer[:20] == expected


@pytest.mark.parametrize("filename, filename_out", [
    ['images/acl1.jpg', 'images/acl1_output.jpg'],
    ['images/acl2.jpg', 'images/acl2_output.jpg'],
    ['images/blank-avatar.jpg', 'images/blank-avatar_output.jpg'],
    ['images/synpic50411.jpg', 'images/synpic50411_output.jpg']
])
def test_b64_string_to_file(filename, filename_out):
    from helper import file_to_b64_string
    from helper import b64_string_to_file
    import filecmp
    import os
    b64str = file_to_b64_string(filename)
    b64_string_to_file(b64str, filename_out)
    answer = filecmp.cmp(filename, filename_out)
    os.remove(filename_out)
    assert answer is True
