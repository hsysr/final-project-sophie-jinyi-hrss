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
