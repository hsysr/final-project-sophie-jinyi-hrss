from flask import Flask, request, jsonify
import requests
import json


server = "http://127.0.0.1:5000"


def retrieve_mrnlist_driver():

    r = requests.get(server + "/api/station/mrnlist")
    mrnlist_int = json.loads(r.text)
    mrnlist = list(map(str, mrnlist_int))
    return mrnlist
