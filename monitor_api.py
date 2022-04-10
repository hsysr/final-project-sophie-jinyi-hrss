from flask import Flask, request, jsonify
import requests
import json


server = "http://127.0.0.1:5000"


def display_mrnlist_driver():
    """ Retrieve list of MRN
    When called in the handler, This function runs which
    retrieves up-to-date MRN list in the database.
    """
    r = requests.get(server + "/api/station/mrnlist")
    mrnlist = json.loads(r.text)
    return mrnlist


def display_record_driver(MRN):
    r = requests.get(server + "/api/station/" + MRN)
    record = json.loads(r.text)
    return record
