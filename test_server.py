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
