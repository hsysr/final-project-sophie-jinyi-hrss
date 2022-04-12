# final-project-sophie-jinyi-hrss

## Author: Sophie Shi, Jinyi Xie

## Intro

This program builds a  a Patient Monitoring System that has a patient-side client,
a monitoring-station client, and a server/database that allows patient data to be
uploaded and stored on the server and retrieved for ad-hoc and continuous monitoring.

## Install

The user should have python installed. 

To create virtual environment, venv library should be installed.
Virtual environment should be set up by:

```
python -m venv venv
```

and activate by:

```
source venv/Scripts/activate
```

After activating the virtual environment, use

```
python -m pip install -r requirements.txt
```

to install required libraries.

## Usage

### Run server and clients
To run the server locally, the server program should be run in the command line by
```
python server.py
```
Currently the server is running on a virtual machine at http://vcm-25959.vm.duke.edu:5000

You could use this address to run requests to GET and POST information to the server. 

To run the patient-side GUI client, type in the command line:

```
python patient_gui.py
```
To run the monitoring station GUI client, type in the command line:

```
python monitor_gui.py
```

To run the server locally, change the `server` variable in `patient_api.py/monitor_api.py` to:
```
server = "http://127.0.0.1:5000"
```

To run the server on the virtual machine, change the `server` variable in `patient_api.py/monitor_api.py` to:
```
server = "http://vcm-25959.vm.duke.edu:5000"
```
### Use patient-side GUI client

In the patient-side GUI window, the user will be asked to enter patient data:

+ Enter patient medical record number in the MRN field. A valid medical record number
  must be an integer.
+ Enter a patient name in the Name field.
+ Select a medical image(.jpg; .png) from local computer. The GUI window will then display a
preview of the medical image.
+ Select an ECG data file
Allow the user to select an ECG data file(.csv) from the local computer.  This
  ECG data is then analyzed for heart rate in beats per minute. This GUI window will then
  display the resulting heart rate, as well as an image of the ECG trace.
+ Click `OK` button to upload the patient info, including the medical record number,
patient name, selected medical image, selected ECG trace and heart rate to the server. In order to
upload the patient info, at least a valid medical record number should be entered.
The information entered will remain in GUI window after uploading.
+ Click `Clear` button to clear all the information entered/selected.
+ Click `Cancel` button to end the program.

## Server Routes

### POST /api/patient/upload

This route is called to upload patient info the server.
The route takes a JSON input as follows:
```
{
        "MRN": <medical_record_number>,
        "name": <patient_name_str>,
        "medical_image": <medical_image_base64_str>,
        "heart_rate": <heart_rate_int>,
        "ECG_image": <ECG_image_base64_str>
}
```
where

* `<medical_record_number>` is a integer containing medical record number
* `<patient_name_str>` is a string containing patient name
* `<medical_image_base64_str>` is a string containing medical image in base64 format
* `<heart_rate_int>` is a integer containing heart rate
* `<ECG_image_base64_str>` is a string containing ECG trace image in base64 format

