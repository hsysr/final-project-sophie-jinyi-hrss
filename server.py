from flask import Flask, request, jsonify
from pymodm import connect, MongoModel, fields


from database import Patient


app = Flask(__name__)


def init_server():
    """Initializes server conditions

    This function initializes the server to connect to the database

    :param: None

    :returns: None
    """
    connect("mongodb+srv://Sophie:bme547@cluster0.yzku1.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority")


def add_patient(input_dict, timestamp):
    """Add new patient to database

    This function add the document of a new patient to mongodb.
    If any information of medical image or ECG is given, this
    information and the corresponding timestamp will also be
    added to the document.

    :param input_dict: dictionary containing the new patient's
                       information
    :param timestamp: str containing the time when the patient
                      is post to the server
    :returns: int containing MRN of the patient added
    """
    p = Patient(MRN=input_dict['MRN'],
                name=input_dict['name'],
                medical_image=[],
                medical_timestamp=[],
                heart_rate=[],
                ECG_image=[],
                ECG_timestamp=[])
    if input_dict['medical_image'] != '':
        p.medical_image.append(input_dict['medical_image'])
        p.medical_timestamp.append(timestamp)
    if input_dict['ECG_image'] != '':
        p.ECG_image.append(input_dict['ECG_image'])
        p.heart_rate.append(input_dict['heart_rate'])
        p.ECG_timestamp.append(timestamp)
    result = p.save()
    return result.MRN


@app.route("/", methods=["GET"])
def status():
    """Server status route

    The function implement the root route and returns
    "Server On" if the server is on

    :param: None

    :returns: None
    """
    return "Server On"


if __name__ == "__main__":
    init_server()
    app.run(host="0.0.0.0")
