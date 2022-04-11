from flask import Flask, request, jsonify
import requests
import json


server = "http://127.0.0.1:5000"


def setup_patient_data(MRN, name, medical_image, heart_rate, ECG_image):
    """setup the patient data to be sent to the server

    This function takes the attributes of a patient's record and put
    them in a dictionary to send to the server in http request.

    :param MRN: int containing the patient's medical record number
    :param name: str containing the patient's name
    :param medical_image: str containing the patient's medical image
                          as base64 string
    :param heart_rate: int containing the patient's average heart
                       rate per minute
    :param ECG_image: str containing the patient's ECG image
                      as base64 string

    :returns: dictionary containing the patient's data for
              uploading
    """
    patient_data = {}
    patient_data['MRN'] = MRN
    patient_data['name'] = name
    patient_data['medical_image'] = medical_image
    patient_data['heart_rate'] = heart_rate
    patient_data['ECG_image'] = ECG_image
    return patient_data


def respond_request(answer, status):
    """handle the server's respond of upload request

    This function takes the reponse and status code from the
    server responding to the upload POST request. It returns
    message to show on patient-side GUI

    :param answer: str containing server's response text
    :param status: int containing the server's responding status code

    :returns: str containing the message to show on GUI
    """
    if status == 200:
        return 'Successfully upload patient data'
    else:
        return answer


def upload_patient_request(patient_data):
    """Make POST request to upload patient information to
    server

    This function takes the patient data as dictionary and
    makes a POST request to the server to upload the patient
    data

    :param patient_data: dictionary containing the patient's
                         data for uploading

    :returns: str containing server's response text
    :returns: int containing the server's responding status code
    """
    global server
    r = requests.post(server + "/api/patient/upload", json=patient_data)
    return r.text, r.status_code
