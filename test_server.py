import pytest


def test_add_patient():
    from server import init_server
    from database import Patient
    from server import add_patient
    init_server()
    info_for_test = 114
    answer = add_patient(info_for_test)
    Patient.objects.raw({"_id": info_for_test}).first().delete()
    assert answer == info_for_test
