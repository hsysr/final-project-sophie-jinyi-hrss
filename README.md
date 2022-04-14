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
### User instruction: patient-side GUI client

In the patient-side GUI window, the user will be asked to enter patient data:

+ Enter patient medical record number in the MRN field. A valid medical record number must be an integer.
+ Enter a patient name in the Name field.
+ Select a medical image(.jpg; .png) from local computer. The GUI window will then display a
preview of the medical image.
+ Select an ECG data file
Allow the user to select an ECG data file(.csv) from the local computer.  This
  ECG data is then analyzed for heart rate in beats per minute. This GUI window will then display the resulting heart rate, as well as an image of the ECG trace.
+ Click `OK` button to upload the patient info, including the medical record number,
patient name, selected medical image, selected ECG trace and heart rate to the server. In order to
upload the patient info, at least a valid medical record number should be entered.
The information entered will remain in GUI window after uploading.
+ Click `Clear` button to clear all the information entered/selected.
+ Click `Cancel` button to end the program.

### User instruction: monitoring station GUI client

In the monitoring station GUI window, the user will be asked to select patient MRN and select the ECG or medical images to view and download. The most recent ECG image would automaticlaly show at the first image chunk.

+ Please select a patient MRN first, otherwise the ECG and medical image list would be blank.
+ After a patient MRN is selected, the most recent ECG image would update automatically if there is new record uploaded to the database. List of the existing ECG and medical images would update automatically, too.
+ Click `Download` button to download the corresponding image. The image would be automatically saved into current folder, and the image name would include the uploaded data and the image type (ECG or medical)
+ Click `Clear` button to clear all the information selected and displayed.
+ Click `Cancel` button to end the program.
+ The status label would show message when you select an MRN or select/download an image.

### Video instruction
You could access the video instruction by the link:
https://duke.box.com/s/iyp1zxx5grmc39ri2bmfean9vr292jty

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

### GET /api/station/mrnlist

This route retrieves the list of existing MRN in the database.
The route return a list of MRN interger.

### GET /api/station/<MRN>

This route retrieves record of the selected MRN as a dictionary in the format as follows:
```
{
        "MRN": <medical_record_number>,
        "name": <patient_name_str>,
        "medical_image": <medical_image_base64_str>,
        "medical_timestamp": <timestamp_medical_image_str>,
        "heart_rate": <heart_rate_int>,
        "ECG_image": <ECG_image_base64_str>,
        "ECG_timestamp": <timestamp_ECG_image_str>
}
```
where

* `<medical_record_number>` is a integer containing medical record number
* `<patient_name_str>` is a string containing patient name
* `<medical_image_base64_str>` is a string containing medical image in base64 format
* `<timestamp_medical image_str>` is a string containing upload datetime of the medical image.
* `<heart_rate_int>` is a integer containing heart rate
* `<ECG_image_base64_str>` is a string containing ECG trace image in base64 format
* `<timestamp_ECG_image_str>` is a string containing upload datetime of the medical image.

The given MRN must be string of integer.

## License
MIT License

Copyright (c) [2022] [Sophie.Shi Jinyi.Xie]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.