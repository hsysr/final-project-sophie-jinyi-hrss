from flask import Flask, request, jsonify
import requests
import json


server = "http://vcm-25959.vm.duke.edu:5000"


def display_mrnlist_driver():
    """ Retrieve list of MRN
    When called in the handler, This function runs which
    retrieves up-to-date MRN list in the database.

    :params: None
    :returns: list of int
    """
    r = requests.get(server + "/api/station/mrnlist")
    mrnlist = json.loads(r.text)
    return mrnlist


def update_record_driver(MRN):
    """ Retrieve record of the selected patient
    When called in the handler, This function runs which
    retrieves patient record according to the MRN
    """
    r = requests.get(server + "/api/station/" + MRN)
    record = json.loads(r.text)
    return record


def generate_filename(timestamp, image_type):
    """ Generate filename for image download
    This function generate the filename of image need to
    be downloaded. The filename contains time and type
    information

    :param timestamp: str containing the timestamp of the image
    :param type: str containing the type of image, would
        be "ECG" or "medical"

    :returns: str, filename of the image to be download
    """
    filename = timestamp[:10] + "_" + image_type + ".jpg"
    return filename
