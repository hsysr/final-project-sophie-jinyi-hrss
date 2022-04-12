from flask import Flask, request, jsonify
from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors
from datetime import datetime
from helper import timestamp_format, validate_input_dict


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


def append_patient_info(patient, input_dict, timestamp):
    """Update patient name, new medical image and ECG
    data of the patient document

    This function update the name of the patient, append
    the new medical image, ECG image and heartrate to
    the patient's document if such data are presented.
    It also append the timestamp when the data is
    received by the server.

    :param input_dict: dictionary containing the new patient's
                       information
    :param timestamp: str containing the time when the patient
                      is post to the server

    :returns: None
    """
    patient.name = input_dict['name']
    if input_dict['medical_image'] != '':
        patient.medical_image.append(input_dict['medical_image'])
        patient.medical_timestamp.append(timestamp)
    if input_dict['ECG_image'] != '':
        patient.ECG_image.append(input_dict['ECG_image'])
        patient.heart_rate.append(input_dict['heart_rate'])
        patient.ECG_timestamp.append(timestamp)


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
    append_patient_info(p, input_dict, timestamp)
    result = p.save()
    return result.MRN


def has_patient(MRN):
    """Determine whether the given patient exists in the database

    This function takes the MRN and check if the patient with
    the given MRN is in the database.

    :param MRN: int containing the medical record number

    :returns: boolean containing whether the given MRN exists
              in the database
    """
    try:
        p = Patient.objects.raw({"_id": MRN}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return True


def update_patient(input_dict, timestamp):
    """Update existing patient to database

    This function update the document of an existing patient
    in the database. If any information of medical image or
    ECG is given, this information and the corresponding
    timestamp will also be added to the document. If a
    patient name is given, the old patient name will be
    replaced by this name.

    :param input_dict: dictionary containing the new patient's
                       information
    :param timestamp: str containing the time when the patient
                      is post to the server

    :returns: Patient containing the patient's updated data
    entry
    """
    p = Patient.objects.raw({"_id": input_dict['MRN']}).first()
    append_patient_info(p, input_dict, timestamp)
    result = p.save()
    return result


def patient_upload_driver(input_dict, timestamp):
    """Implements the /api/patient/upload route to upload patient
    information to the database

    This function implements the /api/patient/upload. The input
    dictionary of the post request is sent to this function as an
    argument, as well as the timestamp when the request was received.
    The function then validate the input dictionary. If the validation
    passes, the function checks whether the patient exists in the
    database. If so, it calls another function to update the information
    of the existing patient. Otherwise, it calls another function to create
    new entry for the patient in the database. The result and status code
    is returned.

    :param input_dict: dictionary containing the new patient's
                       information
    :param timestamp: str containing the time when the patient
                      is post to the server

    :returns: str containing the upload result
    :returns: int containing status code
    """
    if not validate_input_dict(input_dict,
                               {"MRN": [int],
                                "name": [str],
                                "medical_image": [str],
                                "heart_rate": [int],
                                "ECG_image": [str]}):
        return "The input is not a dictionary with correct format", 400
    if has_patient(input_dict['MRN']):
        result = update_patient(input_dict, timestamp)
        return "Updated information of patient #" + str(result.MRN), 200
    result = add_patient(input_dict, timestamp)
    return "Added patient #" + str(result) + " to database", 200


def retrieve_mrnlist_driver():
    """Implements the /api/station/mrnlist route to upload patient
    information to the database

    This function implements the /api/station/mrnlist, it retrieves
    patient MRNs existed in the databse

    :returns: list of integers containing the MRN of all existed patients
    """
    mrnlist = []
    for patient in Patient.objects.raw({}):
        mrnlist.append(patient.MRN)
    return mrnlist, 200


def retrieve_record_driver(MRN):
    """Implements the /api/station/<MRN> route for retrieving
    record of the patient according to given MRN.

    This function implements the /api/station/<MRN> route that should return a
    class that contains the full information of a patient with the given MRN

    It returns patient class as "answer" and a "status_code" from this
    driver function.  Finally, it returns the "answer" using jsonify and the
    status_code.

    :param MRN: integer of the query patient MRN

    :returns: dict of all the record of the patient
    :returns: int of status_code
    """
    from helper import num_parse
    MRN = num_parse(MRN)
    if MRN is None:
        return "MRN is not a valid integer.", 400
    else:
        try:
            patient = Patient.objects.raw({"_id": MRN}).first()
        except pymodm_errors.DoesNotExist:
            return "Patient_id {} was not found".format(MRN), 400
        patient_record = {
            "MRN": patient.MRN,
            "name": patient.name,
            "medical_image": patient.medical_image,
            "medical_timestamp": patient.medical_timestamp,
            "heart_rate": patient.heart_rate,
            "ECG_image": patient.ECG_image,
            "ECG_timestamp": patient.ECG_timestamp}
        return patient_record, 200


@app.route("/", methods=["GET"])
def status():
    """Server status route

    The function implement the root route and returns
    "Server On" if the server is on

    :param: None

    :returns: None
    """
    return "Server On"


@app.route("/api/patient/upload", methods=["POST"])
def patient_upload_handler():
    """Handles request to the /api/patient/upload route for uploading
    patient information

    The /api/patient/upload is a POST request that should receive a
    JSON-encoded string with the following format:
    {
        "MRN": <medical_record_number>,
        "name": <patient_name_str>,
        "medical_image": <medical_image_base64_str>,
        "heart_rate": <heart_rate_int>,
        "ECG_image": <ECG_image_base64_str>
    }
    The function then calls a driver function that implements the functionality
    of this route and receives an "answer" and "status_code" from this
    driver function.  Finally, it returns the "answer" using jsonify and the
    status_code.

    :param: None

    :returns: str containing the return message
    :returns: int containing status code
    """
    input_dict = request.get_json()
    answer, status_code = patient_upload_driver(
        input_dict,
        timestamp_format(datetime.now())
    )
    return jsonify(answer), status_code


@app.route("/api/station/mrnlist", methods=["GET"])
def retrieve_mrnlist_handler():
    """Handles request to the /api/station/mrnlist route for retrieving
    a list of MRN.

    The /api/station/mrnlist  is a GET request that should return a
    JSON-encoded list of MRN existed in the database

    The function then calls a driver function that implements the functionality
    of this route and receives an "answer" and "status_code" from this
    driver function.  Finally, it returns the "answer" using jsonify and the
    status_code.

    :param: None

    :returns: list of integers, containing list of existed patient MRN
    """
    answer, status_code = retrieve_mrnlist_driver()
    return jsonify(answer), status_code


@app.route("/api/station/<MRN>", methods=["GET"])
def retrieve_record_handler(MRN):
    """Handles request to the /api/station/<MRN> route for retrieving
    record of the patient according to given MRN.

    The /api/station/<MRN> is a GET request that should return a
    class that contains the full information of a patient with the given MRN

    The function then calls a driver function that implements the functionality
    of this route and receives an "answer" and "status_code" from this
    driver function.  Finally, it returns the "answer" using jsonify and the
    status_code.

    :param MRN: integer of the query patient MRN

    :returns: dict of all the record of the patient
    :returns: int of status_code
    """
    answer, status_code = retrieve_record_driver(MRN)
    return jsonify(answer), status_code


if __name__ == "__main__":
    init_server()
    app.run(host="0.0.0.0")
