import pytest
from helper import file_to_b64_string


@pytest.mark.parametrize(
    "MRN, name, medical_image, heart_rate, ECG_image, expected",
    [
        [5,
         'Smith.J',
         '',
         -1,
         '',
         {'MRN': 5,
          'name': 'Smith.J',
          'medical_image': '',
          'heart_rate': -1,
          'ECG_image': ''}],
        [7,
         'Hsysr.D',
         'mi_str',
         -1,
         '',
         {'MRN': 7,
          'name': 'Hsysr.D',
          'medical_image': 'mi_str',
          'heart_rate': -1,
          'ECG_image': ''}],
        [5,
         'Smith.J',
         '',
         73,
         'ei_str',
         {'MRN': 5,
          'name': 'Smith.J',
          'medical_image': '',
          'heart_rate': 73,
          'ECG_image': 'ei_str'}],
        [7,
         'Hsysr.D',
         'mi_str',
         60,
         'ei_str',
         {'MRN': 7,
          'name': 'Hsysr.D',
          'medical_image': 'mi_str',
          'heart_rate': 60,
          'ECG_image': 'ei_str'}]
    ])
def test_setup_patient_data(MRN,
                            name,
                            medical_image,
                            heart_rate,
                            ECG_image,
                            expected):
    from patient_api import setup_patient_data
    answer = setup_patient_data(MRN,
                                name,
                                medical_image,
                                heart_rate,
                                ECG_image)
    assert answer == expected
