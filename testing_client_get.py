import requests
import base64


server = "http://127.0.0.1:5000"


r = requests.get(server + "/api/station/mrnlist")
print(r.status_code)
print(r.text)

r = requests.get(server + "/api/station/5")
print(r.status_code)
print(r.text)
