# cloud_server.py

import pymodm.errors
from flask import Flask, request, jsonify
import logging
from pymodm import connect
from database_definitions import Patient
import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from skimage.io import imsave
from skimage.transform import resize
import numpy as np

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def initialize_server():
    """ Initializes server conditions

    This function initializes the server log as well as creates a connection
    with the MongoDB database.
    """
    logging.basicConfig(filename="patient_record_server.log",
                        filemode='w',
                        level=logging.DEBUG)
    print("Connecting to MongoDB...")
    connect("mongodb+srv://mqt3:71IhMxzWnTpAhRkg@bme547.qubox.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority")
    print("Connection attempt finished.")


@app.route("/", methods=["GET"])
def status():
    """Used to indicate that the server is running
    """
    return "Server is on"


@app.route("/api/add_files", methods=["POST"])
def new_patient():
    in_data = request.get_json()
    error_string, status_code = \
        validate_input(in_data, expected_input)
    if error_string is not True:
        return error_string, status_code
    if not find_patient(in_data["record_number"]):
        # Patient does not already exist in database
        add_database_entry(in_data["patient_name"],
                           in_data["record_number"],
                           in_data["medical_image_files"],
                           in_data["medical_images_b64"],
                           in_data["ECG_image_files"],
                           in_data["ECG_images_b64"],
                           in_data["heartrates"],
                           in_data["datetimes"])
        logging.info("Added new patient with id: {}"
                     .format(in_data["record_number"]))
        return "Added patient {}".format(in_data["record_number"])
    else:
        # Patient already exists in database
        add_patient_file(in_data["patient_name"],
                         in_data["record_number"],
                         in_data["medical_image_files"],
                         in_data["medical_images_b64"],
                         in_data["ECG_image_files"],
                         in_data["ECG_images_b64"],
                         in_data["heartrates"],
                         in_data["datetimes"])
        logging.info("Edited info of patient with id: {}"
                     .format(in_data["record_number"]))
        return "Added file for patient {}".format(in_data["record_number"])


@app.route("/api/record_numbers", methods=["GET"])
def id_numbers():
    """ Called to return the medical record numbers in the database

    This is a "GET" route used to retrieve all the medical record
    numbers for all patients currently in the Mongo database. The
    function "list_record_numbers" is used and the returned list
    is jsonified for easy communication. Nothing needs to be
    provided since it is a GET route.
    """
    record_numbers = list_record_numbers()
    return jsonify(record_numbers)


@app.route("/api/get_info", methods=["POST"])
def get_info():
    """ Called to return all information about a specific patient

    This is a "POST" route that takes in a medical record number and
    calls the "retrieve_all_info" function to query the database
    using that record number and return the corresponding Mongo
    database entry. A dictionary is created and the patient
    information is transferred to that dictionary under appropriate
    fields. This dictionary is then jsonified and returned for easy
    communication.
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

    This function first checks if in_data is a dictionary,
    the required type for these route inputs. If not, the
    error string "The input was not a dictionary." is
    returned along with the status code 400.
    Then, it loops through each key in the expected_input
    dictionary and checks to make sure that key is expected
    in the in_data dictionary. If not, an error string
    specifiying which key is missing is returned along with
    the status code 400. For each key that is supposed to
    have an int value associated with it, the function
    checks to make sure the actual value in in_data is an
    int and returns an error message along with the code
    400 if not. If the value is not supposed to be an int,
    the else statement checks to make sure the value in
    in_data corresponding to the key of interest has the
    type specified in expected_input. If not, an error
    string specifying they key with the wrong data type
    is returned along with the code 400. If all these
    checks pass, then the boolean value TRUE will be
    returned along with the status code 200.

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
        invalid input (400 or 401)
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


def check_int(in_data, key):
    """Checks whether the key value is an int

    This function tries to convert the value
    associated with the key parameter in the
    dictionary in_data to an int. If the value
    is an int or is a numeric string, this will
    be successful and the in_data will be
    returned without numeric strings and only
    ints. However, if the value is a string
    containing letters, this int conversion
    will raise a ValueError, which will be
    captured by the try-except block and the
    error message will be returned specifying
    that the value associated with the specified
    key is not an int.

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
    if patient_name == "":
        patient_name = "N/A"
    patient_to_add = Patient(name=patient_name,
                             medical_record_number=id_no)
    patient_to_add.medical_images.append(medical_file)
    patient_to_add.medical_images_b64.append(medical_b64)
    patient_to_add.ecg_images.append(ecg_file)
    patient_to_add.ecg_images_b64.append(ecg_b64)
    patient_to_add.heart_rates.append(bpm)
    patient_to_add.datetimes.append(timestamp)
    answer = patient_to_add.save()
    logging.info("Added new patient into database with id: {}".format(id_no))
    return answer


def find_patient(id_no):
    try:
        patient = Patient.objects.raw({"_id": id_no}).first()
    except pymodm.errors.DoesNotExist:
        patient = False
    return patient


def add_patient_file(patient_name, id_no, medical_file, medical_b64,
                     ecg_file, ecg_b64, bpm, timestamp):
    patient = find_patient(id_no)
    if patient_name != "":
        if patient_name != patient.name:
            logging.warning("Entered patient name does not match "
                            "records for {}. Patient name will now "
                            "be set to {}".format(id_no, patient_name))
            patient.name = patient_name
    if medical_file != "":
        patient.medical_images.append(medical_file)
        patient.medical_images_b64.append(medical_b64)
    if ecg_file != "":
        patient.ecg_images.append(ecg_file)
        patient.ecg_images_b64.append(ecg_b64)
        patient.heart_rates.append(bpm)
        patient.datetimes.append(timestamp)
    patient.save()
    logging.info("Added new file for patient with id: {}".format(id_no))
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


def read_file_as_b64(image_path):
    """Converts an image into a b64 string

       This function takes in the file path for an image
       and then converts that image into a b64 string for
       further processing and storage. This b64 string is
       then returned.

       Parameters
        ----------
        image_path : Str
            Contains the file path to an image

       Returns
       -------
       str
           Containing the converted image as a b64 string
       """
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def b64_string_to_file(b64_string, filewrapper):
    """Converts a b64 string to an an image file

       This function takes in the b64 string representing
       an image, decodes it using the b64decode function from
       the base64 module to convert it into byte format. Then
       a file specified by the user is opened and the bytes
       are written in that file to produce an image file.
       Nothing is returned but the image file will appear locally.

       Parameters
        ----------
        b64_string : Str
            Contains the image in b64 string format
        filewrapper: io.TextIOWrapper object
            Contains information about the name and location for
            the saved image file. This object is returned by the
            asksaveasfilename function, part of filedialogue in
            Tkinter
       """
    image_bytes = base64.b64decode(b64_string)
    with filewrapper as out_file:
        out_file.write(image_bytes)
    return None


def b64_to_ndarray(b64):
    """Converts a b64 string into an ndarray

       This function takes in the b64 string representing an
       image file. Then it is converted to an ndarray using
       functions from the base64 and io modules. This ndarray
       representation of the iamge is then returned for
       resizing or displaying purposes.

       Parameters
        ----------
        b64 : Str
            Contains the image in b64 string format

       Returns
       -------
       array
           Containing the converted image as a ndarray
       """
    image_bytes = base64.b64decode(b64)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def get_index(listvar, val):
    """Gets the index of a specified value in a given list

       This function takes in a value and a list and simply
       searches the list using the index function for the
       specified value.

       Parameters
        ----------
        listvar : list
            A list containing any type of values to be searched
        val : Any type
            A specific value of any type that will be searched
            for in the list passed in

       Returns
       -------
       int
           Containing the index of the value in the list
       """
    index = listvar.index(val)
    return index


def resize_image(nd):
    """resizes an image in ndarray form to 250x250

       This function takes in an ndarray representing an image
       and resizes it to be 250x250. This way, all images are uniform
       in size, so the GUI does not constantly change shape or become
       too large. The resized ndarray is then returned

       Parameters
        ----------
        nd : array
            An ndarray representing an image

       Returns
       -------
       array
           Containing the ndarray representing the resized image
       """
    resized_nd = resize(nd, (250, 250)) * 255
    resized_nd = resized_nd.astype(np.uint8)
    return resized_nd


if __name__ == '__main__':
    initialize_server()

    # path = "/Users/michael.tian/Desktop/BME 547/class_repos" \
    #        "/final-project-spooky-dookie/images/"
    # images = ["acl1.jpg", "acl2.jpg", "esophagus 1.jpg", "esophagus2.jpg",
    #           "synpic50411.jpg", "synpic51041.jpg", "synpic51042.jpg",
    #           "upj1.jpg", "upj2.jpg", "test_ECG.jpg", "test_tachycardia.jpg"]
    # full_path = []
    # for i in range(len(images)):
    #     full_path.append(path + images[i])
    # b64_images = []
    # for i in full_path:
    #     b64_images.append(read_file_as_b64(i))
    # datetimes = ["2020-03-00 11:00:36", "2020-03-01 11:00:36",
    #              "2020-03-02 11:00:36"]
    # patient1 = Patient("Yume Choi", 3, ["acl1.png"], [b64_images[6]],
    #                    [images[9]], [b64_images[-2]], [85], [datetimes[0]])
    # patient2 = Patient("Michael Tian", 5, images[0:9], b64_images[0:9],
    #                    images[9:], b64_images[9:], [85, 90], datetimes[1:])
    # patient3 = Patient("Phoebe Dijour", 11, ["acl1.png", "acl2.png"],
    #                    [b64_images[2], b64_images[3]], [images[10]],
    #                    [b64_images[-1]], [85], [datetimes[0]])
    # patient1.save()
    # patient2.save()
    # patient3.save()

    app.run()
