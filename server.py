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


def add_patient(MRN):
    """Add new patient to database

    This function add the document of a new patient to mongodb.
    The new document has the given MRN, and other fields are
    set to blank.

    :param MRN: int containing the patient's medical record number

    :returns: int containing MRN of the patient added
    """
    p = Patient(MRN=MRN,
                name='',
                medical_image=[],
                medical_timestamp=[],
                heart_rate=[],
                ECG_image=[],
                ECG_timestamp=[])
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
