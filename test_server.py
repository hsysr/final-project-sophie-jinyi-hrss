import pytest
from server import init_server


init_server()


def test_add_patient():
    from database import Patient
    from server import add_patient
    info_for_test = {
        'MRN': 114523,
        'name': 'Smith.J',
        'medical_image': '',
        'ECG_image': '',
        'heart_rate': -1
    }
    answer = add_patient(info_for_test, "2022-04-05 16:09:26")
    Patient.objects.raw({"_id": info_for_test['MRN']}).first().delete()
    assert answer == info_for_test['MRN']


def test_has_patient():
    from database import Patient
    from server import has_patient
    test_patient = Patient(MRN=114523,
                           name='Smith.J',
                           medical_image=[],
                           medical_timestamp=[],
                           heart_rate=[],
                           ECG_image=[],
                           ECG_timestamp=[])
    test_patient.save()
    assert has_patient(test_patient.MRN) is True
    assert has_patient(114) is False
    Patient.objects.raw({"_id": test_patient.MRN}).first().delete()


def test_update_patient():
    from database import Patient
    from server import update_patient
    test_patient = Patient(MRN=114523,
                           name='Smith.J',
                           medical_image=[],
                           medical_timestamp=[],
                           heart_rate=[],
                           ECG_image=[],
                           ECG_timestamp=[])
    test_patient.save()
    test_update_info = {
        'MRN': 114523,
        'name': 'Smith.F',
        'medical_image': 'some base64 string',
        'ECG_image': 'some base64 string',
        'heart_rate': 72
    }
    test_timestamp = "2022-04-05 16:09:26"
    answer = update_patient(test_update_info, test_timestamp)
    assert answer.MRN == test_update_info['MRN']
    assert answer.name == test_update_info['name']
    assert answer.medical_image == [test_update_info['medical_image']]
    assert answer.medical_timestamp == [test_timestamp]
    assert answer.heart_rate == [test_update_info['heart_rate']]
    assert answer.ECG_image == [test_update_info['ECG_image']]
    assert answer.ECG_timestamp == [test_timestamp]
    Patient.objects.raw({"_id": test_patient.MRN}).first().delete()
