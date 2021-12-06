# BME 547 Final Project

Patient Monitoring Client/Server Project

BME 547 Final Project - Michael Tian and Phoebe Dijour

A detailed README describing the final performance and state of your project. This should include a basic instruction manual for your GUI clients, an API reference guide for your server, and a description of your database structure.

The purpose of this project is to design a Patient Monitoring System that has a patient-side GUI, a monitoring-station GUI, and a server/database that allows patient data to be uploaded and stored on the server and retrieved for ad-hoc and continuous monitoring. This can be used in a medical setting, where patients and medical professionals can enter medical images and ECG files into a patient-side GUI. This GUI interacts with a server and a database to store patient information. Then, a patient or medical professional can use the monitoring-station GUI to see each patient's medical files, including any timestamped heart rates that were calculated based on the ECG files. Read on for more information about the project.

## Basic instruction manual
### Setting up
1. The cloud server script will be running on a virtual machine which can be accessed using the following url: `vcm-23074.vm.duke.edu`
2. Patients will upload their information using the `patient_GUI`, and providers on the other hand will need to have both the `cloud_client` script as well as the `provider_GUI` script.
3. In order for a provider to user the `provider_GUI`, there should be at least one patient in the database.


### Using Patient-Side GUI (patient_GUI.py)
There are four different fields that you can manipulate. You can type in the patient name and medical record number and search for a medical image file and an ECG .csv file from dialog boxes. Here are more detailed instructions:
1. Type in the patient name and/or record number. The record number is the only field that is absolutely necessary to include before uploading, or else the GUI will return an error. If the name entered for a particular record number is different from the one in the database, the name will update, and a warning will be logged.
2. Click the "Select Image" buttons for the medical image or ECG image. This opens a file dialog box that allows you to select an image with the appropriate type (.jpeg, .jpg, or .png for medical image and .csv for ECG file). Select a file. The GUI will immediately display the chosen image along with the filename. If you selected an ECG file, the GUI will dispaly the calcualted heart rate. If you press "Cancel" instead of selecting a file, a message box will appear that notifies the user they have decided to cancel image selection.
3. In order to remove an image from the GUI, click the "Clear Image" button for the corresponding image.
4. Once you have included all of the information you wish to upload, press the "Upload" button, which sends information to the survey and dispalys a return message below the button.
5. Click the "Cancel" button to close the GUI window.


### Using Monitoring Station GUI (provider_GUI.py)
There are three different fields that the user can manipulate. You can select a patient record number and select medical and ECG images. You can also choose to save the image files to your computer. Here are more detailed instructions:
1. Click on the patient medical record number dropdown menu to see all of the record numbers in the database. Choose which record number you wish to view data for.
2. Once you choose a number, it will automatically populate the patient name, medical record number, latest heart rate, and latest ECG trace timestamp and iamge items.
3. Click on the medical image dropdown menu to see of the of the medical image file names for the chosen patient. Choose which image you wish to view.
4. Click on the historical ECG image dropdown menu to see of the of the ECG image file names for the chosen patient. Choose which image you wish to view.
5. Press the "Save" button below any of the images to save them to your computer.
6. Click the "Cancel" button to close the GUI window.


## API Reference Guide for Server
This Flask server contains several API routes. Here are the routes that require a client POST request to the server:

* `http://152.3.65.89:5001/api/add_files` adds patient information to the database by taking the following JSON from the patient-side GUI:
  ```
  {
      "patient_name": "Phoebe Dijour",
      "record_number": 4,
      "medical_image_files": "esophagus.jpg",
      "medical_images_b64": "./012345abcde",
      "ECG_image_files": "ecg_2.png",
      "ECG_images_b64": "./678910fghijk",
      "heartrates": 84,
      "datetimes": "2021-03-09 11:00:36"  
  }
  ```

* `http://152.3.65.89:5001/api/get_info` takes in a medical record number and queries the database to return the corresponding Mongo database entry for the record number. It returns the following JSON dictionary:
  ```
  {
      "name": "Phoebe Dijour",
      "medical_record_number": 4,
      "medical_images": ["intestine.jpeg", "throat.png", "esophagus.jpg"],
      "medical_images_b64": ["./abcde012345", "./ABCDE98765", "./012345abcde"],
      "ecg_images": ["ecg_1.png", "ecg_2.png"],
      "ecg_images_b64": ["./fghijk678910", "./678910fghijk"],
      "heart_rates": [76, 84],
      "datetimes": ["2020-09-14 12:16:32", "2021-03-09 11:00:36"]}
  }
  ```

Here are the routes that can be accessed by a local client program through GET requests:

* `http://152.3.65.89:5001/api/` returns a string that states that the server is on:
  ```
  "Server is on"
  ```

* `http://152.3.65.89:5001/api/record_numbers` returns a JSON list of record numbers for all patients in the database, like this:
  ```
  [9, 4, 6, 8]
  ```


## Database Structure
For this program we are using a non-relational database called MongoDB. Our Python code accesses the database by making requests to the MongoDB database API using a package called PyMODM. This not only gives us access to the MongoDB API, but also enforces type-checking.

Database definitions
* name = fields.CharField()
* medical_record_number = fields IntegerField(primary_key=True)
* medical_images = fields.ListField()
* medical_images_b64 = fields.ListField()
* ecg_images = fields.ListField()
* ecg_images_b64 = fields.ListField()
* heart_rates = fields.ListField()
* datetimes = fields.ListField()


## Logging
The server writes to a log file called `HeartRate.log` when the following events occur:

* New patient added = INFO log
* Patient updated = INFO log
* Patient's name entry different from patient name in database = WARNING log


## Status Codes
The following status codes are used in the server:
* 200: successful attempt
* 400: bad request / bad input format


## Virtual Machine
* Hostname: vcm-23074.vm.duke.edu
* Port: 5001


## MIT License

Copyright (c) 2021 Phoebe Dijour, Michael Tian

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.