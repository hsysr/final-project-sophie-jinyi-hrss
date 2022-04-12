import pytest


@pytest.mark.parametrize(
    "timestamp, image_type, expected",
    [
        ["2022-04-11 15:54:40", "ECG",
         "2022-04-11_ECG.jpg"],
        ["2022-04-11 15:30:25", "medical",
         "2022-04-11_medical.jpg"]
    ])
def test_generate_filename(timestamp, image_type, expected):
    from monitor_api import generate_filename
    answer = generate_filename(timestamp, image_type)
    assert answer == expected
