import requests
import base64
import json


server = "http://127.0.0.1:5000"


r = requests.get(server + "/api/station/mrnlist")
print(r.status_code)
print(r.text)
a = json.loads(r.text)
print(a[0])

r = requests.get(server + "/api/station/5")
print(r.status_code)
# print(r.text)
b = json.loads(r.text)
print(b["ECG_timestamp"][-1])
print(b["ECG_timestamp"].index("2022-04-07 20:18:43"))
