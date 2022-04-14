import pytest


@pytest.mark.parametrize(
    "timestamp, image_type, expected",
    [
        ["2022-04-11 15:54:40", "ECG",
         "2022_04_11_15_54_40_ECG.jpg"],
        ["2022-04-11 15:30:25", "medical",
         "2022_04_11_15_30_25_medical.jpg"]
    ])
def test_generate_filename(timestamp, image_type, expected):
    from monitor_api import generate_filename
    answer = generate_filename(timestamp, image_type)
    assert answer == expected
