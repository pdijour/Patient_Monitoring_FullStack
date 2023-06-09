# cloud_server.py

import pymodm.errors
from flask import Flask, request, jsonify
import logging
from pymodm import connect
from database_definitions import Patient
from cloud_client import convert_file_to_b64_string
import base64
import io
import matplotlib.image as mpimg
from skimage.transform import resize
import numpy as np

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def initialize_server():
    """Initializes server conditions

    This function initializes the server log as well as creates a connection
    with the MongoDB database. It prints when the server is connecting to the
    database and once is has successfuly connected.
    """
    logging.basicConfig(filename="patient_record_server.log",
                        filemode='w',
                        level=logging.DEBUG)
    print("Connecting to MongoDB...")
    connect("mongodb+srv://pdijour:mongopassword@bme547.vwsmd.mongodb.net/"
            "final_project?retryWrites=true&w=majority")
    print("Connection attempt finished.")


@app.route("/", methods=["GET"])
def status():
    """Used to indicate that the server is running

       This function makes a GET request that simply returns "Server is on" if
       the server is running.

       Returns
       -------
       String
           Containing message that the server is on
       """
    return "Server is on"


@app.route("/api/add_files", methods=["POST"])
def new_patient():
    """Called to add information to the database based on GUI inputs

       This is a "POST" route used to get data from the GUI in the form of a
       dictionary. This function then calls an external function "new_or_old"
       that determines if the uploaded information matches a patient that is
       already in the database or not. It returns an answer that says if a
       patient was added or updated and which patient it was.

       Returns
       -------
       String
           Containing message that there was an error, patient was added, or
           patient was updated
       """
    in_data = request.get_json()
    answer = new_or_old(in_data)
    return answer


@app.route("/api/record_numbers", methods=["GET"])
def id_numbers():
    """Called to return the medical record numbers in the database

       This is a "GET" route used to retrieve all the medical record
       numbers for all patients currently in the Mongo database. The
       function "list_record_numbers" is used and the returned list
       is jsonified for easy communication. Nothing needs to be
       provided since it is a GET route.

       Returns
       -------
       JSON String
           Containing medical record numbers for all patients in the database
       """
    record_numbers = list_record_numbers()
    return jsonify(record_numbers)


@app.route("/api/get_info", methods=["POST"])
def get_info():
    """Called to return all information about a specific patient

       This is a "POST" route that takes in a medical record number and
       calls the "retrieve_all_info" function to query the database
       using that record number and return the corresponding Mongo
       database entry. A dictionary is created and the patient
       information is transferred to that dictionary under appropriate
       fields. This dictionary is then jsonified and returned for easy
       communication.

       Returns
       -------
       JSON String
           Containing a dictionary of the patient's information that
           corresponds to the medical record number
       """
    in_data = request.get_json()
    info = retrieve_all_info(in_data)
    return jsonify(info)


expected_input = {"patient_name": str,
                  "record_number": int,
                  "medical_image_files": str,
                  "medical_images_b64": str,
                  "ECG_image_files": str,
                  "ECG_images_b64": str,
                  "heartrates": int,
                  "datetimes": str}


def validate_input(in_data, expected_input):
    """Determines whether an input is valid to a route

       This function first checks if in_data is a dictionary, the required type
       for these route inputs. If not, the error string "The input was not a
       dictionary." is returned along with the status code 400. Then, it loops
       through each key in the expected_input dictionary and checks to make
       sure that key is expected in the in_data dictionary. If not, an error
       string specifiying which key is missing is returned along with the
       status code 400. For each key that is supposed to have an int value
       associated with it, the function checks to make sure the actual value in
       in_data is an int and returns an error message along with the code 400
       if not. If the value is not supposed to be an int, the else statement
       checks to make sure the value in in_data corresponding to the key of
       interest has the type specified in expected_input. If not, an error
       string specifying they key with the wrong data type is returned along
       with the code 400. If all these checks pass, then the boolean value
       TRUE will be returned along with the status code 200.

       Parameters
        ----------
       in_data : Dict
           Contains the input data to a route
       expected_input : Dict
           Contains the expected format of the in_data including
           all keys and corresponding data types for values

       Returns
       -------
       String
           Containing relevant error message if invalid input
       Boolean
           Containing 'TRUE' value if valid input
       Int
           Status code corresponding to valid (200) or
           invalid input (400)
       """
    if type(in_data) is not dict:
        return "The input was not a dictionary.", 400
    if in_data["record_number"] == "":
        return "The key record_number is empty", 400
    for key in expected_input:
        if key not in in_data:
            return "The key {} is missing from input".format(key), 400
        if expected_input[key] == int:
            if in_data[key] != "":
                val = check_int(in_data, key)
                if type(val) == str:
                    return val, 400
        else:
            if type(in_data[key]) is not expected_input[key]:
                return "The key {} has the wrong data type".format(key), 400
    return True, 200


def new_or_old(in_data):
    """Checks if the patient is already in the database and executes functions
       to add or update patient in database

       This function first validates that the input is in the correct format
       using the validate_input function. It then uses the find_patient
       function to determine if the patient already exists in the database
       using the patient's medical record number. If the patient does not exist
       in the database, this function calls the add_database_entry function and
       returns a message that the patient was added. If the patient does exist
       in the database, this function calls the add_patient_file function and
       returns a message that the patient was updated.

       Parameters
       ----------
       in_data : Dict
           Contains the input data to a route

       Returns
       -------
       String
           Containing relevant error message if not an int
       Dict
           Containing the input data with int value confirmed
       """
    error_string, status_code = validate_input(in_data, expected_input)
    if error_string is not True:
        return error_string, status_code
    if not find_patient(in_data["record_number"]):
        add_database_entry(in_data["patient_name"],
                           in_data["record_number"],
                           in_data["medical_image_files"],
                           in_data["medical_images_b64"],
                           in_data["ECG_image_files"],
                           in_data["ECG_images_b64"],
                           in_data["heartrates"],
                           in_data["datetimes"])
        return "Added patient {}".format(in_data["record_number"])
    else:
        add_patient_file(in_data["patient_name"],
                         in_data["record_number"],
                         in_data["medical_image_files"],
                         in_data["medical_images_b64"],
                         in_data["ECG_image_files"],
                         in_data["ECG_images_b64"],
                         in_data["heartrates"],
                         in_data["datetimes"])
        return "Updated patient {}".format(in_data["record_number"])


def check_int(in_data, key):
    """Checks whether the key value is an int

       This function tries to convert the value associated with the key
       parameter in the dictionary in_data to an int. If the value is an int or
       is a numeric string, this will be successful and the in_data will be
       returned without numeric strings and only ints. However, if the value is
       a string containing letters, this int conversion will raise a
       ValueError, which will be captured by the try-except block and the error
       message will be returned specifying that the value associated with the
       specified key is not an int.

       Parameters
       ----------
       in_data : Dict
           Contains the input data to a route
       key : Str
           Contains the key whose value will be checked

       Returns
       -------
       String
           Containing relevant error message if not an int
       Dict
           Containing the input data with int value confirmed
       """
    err_msg = "The value corresponding to the key {} " \
              "is not an integer.".format(key)
    try:
        in_data[key] = int(in_data[key])
    except ValueError:
        return err_msg
    return in_data


def add_database_entry(patient_name, id_no, medical_file, medical_b64,
                       ecg_file, ecg_b64, bpm, timestamp):
    """Adds patient to database using GUI inputs

       This function uses the GUI inputs (patient name, medical record number,
       medical image file name, medical image b64 string, ecg image file name,
       ecg image b64 string, heart rate, and timestamp of heart rate) to add a
       patient to the database. If a name was not entered, the name defaults to
       "N/A". Once the name is specified, a Patient object is created with the
       name and medical record number of the patient. Then, if the medical
       image file name is not an empty string, meaning the user has selected an
       image, the function adds the medical image file name and the b64 string
       to the database. Similarly, if the ECG image file name is not an empty
       string, meaning that the user has selected an image, the function adds
       the ECG image file name, the b64 string, the heart rate, and the
       timestamp to the database. It then saves the patient and logs that a
       new patient has been entered into the database. It returns the patient
       that has been saved.

       Parameters
       ----------
        patient_name : Str
            Contains the patient's name
        id_no : int
            Contains the patient's medical record / ID number
        medical_file : Str
            Contains the file name of the medical image
        medical_b64 : Str
            Contains the b64 string of the medical image
        ecg_file : Str
            Contains the file name of the ecg image
        ecg_b64 : Str
            Contains the b64 string of the ecg image
        bpm : int
            Contains the heart rate for the chosen ecg file
        timestamp : Str
            Contains the date and time that the heart rate was determined

       Returns
       -------
       Patient object
           Containing the patient that was added to the database
       """
    if patient_name == "":
        patient_name = "N/A"
    patient_to_add = Patient(name=patient_name,
                             medical_record_number=id_no)
    if medical_file != "":
        patient_to_add.medical_images.append(medical_file)
        patient_to_add.medical_images_b64.append(medical_b64)
    if ecg_file != "":
        patient_to_add.ecg_images.append(ecg_file)
        patient_to_add.ecg_images_b64.append(ecg_b64)
        patient_to_add.heart_rates.append(bpm)
        patient_to_add.datetimes.append(timestamp)
    answer = patient_to_add.save()
    logging.info("Added new patient into database with id: {}".format(id_no))
    return answer


def find_patient(id_no):
    """Finds if patient exists in database already based on ID number

       This function uses the GUI inputs of medical record number to determine
       if the number is already present in one of the patient's
       medical_record_number attributes. It implements a try except block to do
       this, and if there is a pymodm error that the medical_record_number
       does not exist, it returns a False boolean. Otherwise, it returns the
       Patient object with the medical record number.

       Parameters
       ----------
        id_no : int
            Contains the patient's medical record / ID number

       Returns
       -------
       Patient object
           Containing the patient that was found in the database
    """
    try:
        patient = Patient.objects.raw({"_id": id_no}).first()
    except pymodm.errors.DoesNotExist:
        patient = False
    return patient


def add_patient_file(patient_name, id_no, medical_file, medical_b64,
                     ecg_file, ecg_b64, bpm, timestamp):
    """Updates patient information in database using GUI inputs

       This function uses the GUI inputs (patient name, medical record number,
       medical image file name, medical image b64 string, ecg image file name,
       ecg image b64 string, heart rate, and timestamp of heart rate) to update
       a patient's information in the database. It first uses the find_patient
       function to return the Patient object with the correct medical record
       number. If the new patient name that was entered is not an empty string,
       it checks if the new patient name matches the patient name that already
       exists in the database. If it does not match, it changes the patient
       name to the most recently entered name and logs a warning that the
       patient's name has changed. Then, if the medical image file name is not
       an empty string, meaning the user has selected an image, the function
       adds the medical image file name and the b64 string to the database.
       Similarly, if the ECG image file name is not an empty string, meaning
       that the user has selected an image, the function adds the ECG image
       file name, the b64 string, the heart rate, and the timestamp to the
       database. It then saves the patient and logs that a patient has been
       updated in the database. It returns the patient that has been updated.

       Parameters
       ----------
        patient_name : Str
            Contains the patient's name
        id_no : int
            Contains the patient's medical record / ID number
        medical_file : Str
            Contains the file name of the medical image
        medical_b64 : Str
            Contains the b64 string of the medical image
        ecg_file : Str
            Contains the file name of the ecg image
        ecg_b64 : Str
            Contains the b64 string of the ecg image
        bpm : int
            Contains the heart rate for the chosen ecg file
        timestamp : Str
            Contains the date and time that the heart rate was determined

       Returns
       -------
       Patient object
           Containing the patient that was added to the database
       """
    patient = find_patient(id_no)
    if patient_name != "":
        if patient_name != patient.name:
            patient.name = patient_name
            logging.warning("Entered patient name does not match "
                            "records for {}. Patient name will now "
                            "be set to {}".format(id_no, patient_name))
    if medical_file != "":
        patient.medical_images.append(medical_file)
        patient.medical_images_b64.append(medical_b64)
    if ecg_file != "":
        patient.ecg_images.append(ecg_file)
        patient.ecg_images_b64.append(ecg_b64)
        patient.heart_rates.append(bpm)
        patient.datetimes.append(timestamp)
    patient.save()
    logging.info("Updated patient with id: {}".format(id_no))
    return patient


def list_record_numbers():
    """Retrieves medical record numbers for all database entries

       This function queries the Mongo database to receive all
       database entries as an iterable. Then, it parses through
       each one and appends the medical record number of each
       entry into a list. Finally, this list is returned.

       Returns
       -------
       List
           Containing record numbers as strings for all database entries
       """
    results = Patient.objects.raw({})
    all_record_numbers = []
    for item in results:
        all_record_numbers.append(item.medical_record_number)
    return all_record_numbers


def retrieve_all_info(id_no):
    """Retrieves all information for a specific database entry

       This function queries the Mongo database using the
       medical record number passed in as a parameter to receive
       all the information in the database about that patient.
       It then creates a dictionary to store all the information
       for the patient in appropriate keys and then returns
       that dictionary.

       Parameters
        ----------
        id_no : Str
            Contains the medical record number of interest

       Returns
       -------
       Dict
           Containing all the information stored in the database
           about the patient specified by the record number
       """
    patient = Patient.objects.raw({"_id": id_no}).first()
    info = {"name": patient.name,
            "medical_record_number": patient.medical_record_number,
            "medical_images": patient.medical_images,
            "medical_images_b64": patient.medical_images_b64,
            "ecg_images": patient.ecg_images,
            "ecg_images_b64": patient.ecg_images_b64,
            "heart_rates": patient.heart_rates,
            "datetimes": patient.datetimes}
    return info


if __name__ == '__main__':
    initialize_server()
    app.run(host="0.0.0.0", port=5002)
