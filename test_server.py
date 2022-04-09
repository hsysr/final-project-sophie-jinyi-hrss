import pytest
from pymodm import connect


connect("mongodb+srv://Sophie:bme547@cluster0.yzku1.mongodb.net/"
        "test_final?retryWrites=true&w=majority")


@pytest.mark.parametrize("info_for_test", [
    {'MRN': 114520,
     'name': 'Smith.J',
     'medical_image': 'some medical_image',
     'ECG_image': 'some ECG_image',
     'heart_rate': 72},
    {'MRN': 114520,
     'name': 'Smith.J',
     'medical_image': '',
     'ECG_image': 'some ECG_image',
     'heart_rate': 72},
    {'MRN': 114520,
     'name': 'Smith.J',
     'medical_image': 'some medical_image',
     'ECG_image': '',
     'heart_rate': -1},
])
def test_add_patient(info_for_test):
    from database import Patient
    from server import add_patient
    answer = add_patient(info_for_test, "2022-04-05 16:09:26")
    Patient.objects.raw({"_id": info_for_test['MRN']}).first().delete()
    assert answer == info_for_test['MRN']


def test_has_patient():
    from database import Patient
    from server import has_patient
    test_patient = Patient(MRN=114522,
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


@pytest.mark.parametrize("test_update_info, expt_ans", [
    [{'MRN': 114523,
      'name': 'Smith.F',
      'medical_image': 'some medical_image',
      'ECG_image': 'some ECG_image',
      'heart_rate': 72},
     {'MRN': 114523,
      'name': 'Smith.F',
      'medical_image': ['some medical_image'],
      'medical_timestamp': ["2022-04-05 16:09:26"],
      'ECG_image': ['some ECG_image'],
      'heart_rate': [72],
      'ECG_timestamp': ["2022-04-05 16:09:26"]}],
    [{'MRN': 114523,
      'name': '',
      'medical_image': 'some medical_image',
      'ECG_image': 'some ECG_image',
      'heart_rate': 72},
     {'MRN': 114523,
      'name': 'Smith.J',
      'medical_image': ['some medical_image'],
      'medical_timestamp': ["2022-04-05 16:09:26"],
      'ECG_image': ['some ECG_image'],
      'heart_rate': [72],
      'ECG_timestamp': ["2022-04-05 16:09:26"]}],
    [{'MRN': 114523,
      'name': 'Smith.F',
      'medical_image': '',
      'ECG_image': 'some ECG_image',
      'heart_rate': 72},
     {'MRN': 114523,
      'name': 'Smith.F',
      'medical_image': [],
      'medical_timestamp': [],
      'ECG_image': ['some ECG_image'],
      'heart_rate': [72],
      'ECG_timestamp': ["2022-04-05 16:09:26"]}],
    [{'MRN': 114523,
      'name': 'Smith.F',
      'medical_image': 'some medical_image',
      'ECG_image': '',
      'heart_rate': -1},
     {'MRN': 114523,
      'name': 'Smith.F',
      'medical_image': ['some medical_image'],
      'medical_timestamp': ["2022-04-05 16:09:26"],
      'ECG_image': [],
      'heart_rate': [],
      'ECG_timestamp': []}]
])
def test_update_patient(test_update_info, expt_ans):
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
    test_timestamp = "2022-04-05 16:09:26"
    answer = update_patient(test_update_info, test_timestamp)
    assert answer.MRN == expt_ans['MRN']
    assert answer.name == expt_ans['name']
    assert answer.medical_image == expt_ans['medical_image']
    assert answer.medical_timestamp == expt_ans['medical_timestamp']
    assert answer.heart_rate == expt_ans['heart_rate']
    assert answer.ECG_image == expt_ans['ECG_image']
    assert answer.ECG_timestamp == expt_ans['ECG_timestamp']
    Patient.objects.raw({"_id": test_patient.MRN}).first().delete()


@pytest.mark.parametrize("input_dict, expt_ans, expt_code", [
    [{"MRN": 114535,
      "name": 'Smith.J',
      "medical_image": '',
      "heart_rate": -1,
      "ECG_image": ''},
     "Added patient #114535 to database",
     200],
    [{"MRN": 114535,
      "name": 'Smith.J',
      "medical_image": '/9j/4AAQSkZJRgABAgAAAQABAAD/2',
      "heart_rate": 72,
      "ECG_image": '/9j/4AAQSkZJRgABAgAAAQAB'},
     "Updated information of patient #114535",
     200],
    [{"MRN": '114535',
      "name": 'Smith.J',
      "medical_image": '/9j/4AAQSkZJRgABAgAAAQABAAD/2',
      "heart_rate": 72,
      "ECG_image": '/9j/4AAQSkZJRgABAgAAAQAB'},
     "The input is not a dictionary with correct format",
     400],
    [{"name": 'Smith.J',
      "medical_image": '/9j/4AAQSkZJRgABAgAAAQABAAD/2',
      "heart_rate": 72,
      "ECG_image": '/9j/4AAQSkZJRgABAgAAAQAB'},
     "The input is not a dictionary with correct format",
     400]
])
def test_patient_upload_driver(input_dict, expt_ans, expt_code):
    from server import patient_upload_driver
    from database import Patient
    answer, status_code = patient_upload_driver(input_dict,
                                                "2022-04-05 16:09:26")
    assert answer == expt_ans
    assert status_code == expt_code
    if answer[:7] == "Updated":
        Patient.objects.raw({"_id": input_dict['MRN']}).first().delete()


def test_retrieve_mrnlist_driver():
    from server import retrieve_mrnlist_driver
    from database import Patient
    from helper import file_to_b64_string
    test_patient = Patient(
        MRN=2,
        name='Alex.M',
        medical_image=[],
        medical_timestamp=[],
        heart_rate=[],
        ECG_image=[],
        ECG_timestamp=[])
    test_patient.save()
    test_patient2 = Patient(
        MRN=5,
        name='Alex.M',
        medical_image=[file_to_b64_string('images/acl1.jpg'),
                       file_to_b64_string('images/acl2.jpg')],
        medical_timestamp=[],
        heart_rate=[],
        ECG_image=[],
        ECG_timestamp=[])
    test_patient2.save()
    answer, status_code = retrieve_mrnlist_driver()
    Patient.objects.raw({"_id": 2}).first().delete()
    Patient.objects.raw({"_id": 5}).first().delete()
    assert answer == [2, 5]
    assert status_code == 200


def test_retrieve_patient_driver():
    from server import retrieve_patient_driver
    from database import Patient
    from helper import file_to_b64_string
    test_patient = Patient(
        MRN=2,
        name='Alex.M',
        medical_image=[],
        medical_timestamp=[],
        heart_rate=[],
        ECG_image=[],
        ECG_timestamp=[])
    test_patient.save()
    test_patient2 = Patient(
        MRN=5,
        name='Alex.M',
        medical_image=[file_to_b64_string('images/acl1.jpg'),
                       file_to_b64_string('images/acl2.jpg')],
        medical_timestamp=[],
        heart_rate=[],
        ECG_image=[],
        ECG_timestamp=[])
    test_patient2.save()
    answer, status_code = retrieve_patient_driver(2)
    answer1, status_code1 = retrieve_patient_driver("2")
    answer2, status_code2 = retrieve_patient_driver("8")
    answer3, status_code3 = retrieve_patient_driver("5r")
    answer4, status_code4 = retrieve_patient_driver("5")
    Patient.objects.raw({"_id": 2}).first().delete()
    Patient.objects.raw({"_id": 5}).first().delete()
    assert answer == test_patient
    assert status_code == 200
    assert answer1 == test_patient
    assert status_code1 == 200
    assert answer2 == "Patient_id 8 was not found"
    assert status_code2 == 400
    assert answer3 == "MRN is not a valid integer."
    assert status_code3 == 400
    assert answer4 == test_patient2
    assert status_code4 == 200
