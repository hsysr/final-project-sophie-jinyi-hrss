import pytest


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
