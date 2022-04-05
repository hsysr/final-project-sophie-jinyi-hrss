import requests
import base64


server = "http://127.0.0.1:5000"


def img2b64(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


new_patient = {"MRN": 5,
               "name": 'Smith.J',
               "medical_image": '',
               "heart_rate": -1,
               "ECG_image": ''}
r = requests.post(server + "/api/patient/upload", json=new_patient)
print(r.status_code)
print(r.text)


mi = img2b64('images/acl1.jpg')
ei = img2b64('images/upj1.jpg')
new_patient = {"MRN": 5,
               "name": 'Smith.F',
               "medical_image": mi,
               "heart_rate": 72,
               "ECG_image": ei}
r = requests.post(server + "/api/patient/upload", json=new_patient)
print(r.status_code)
print(r.text)
