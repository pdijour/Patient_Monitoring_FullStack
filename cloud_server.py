# cloud_server.py

import pymodm.errors
from flask import Flask, request, jsonify
import logging
from pymodm import connect
from database_definitions import Patient

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def initialize_server():
    """ Initializes server conditions

    This function initializes the server log as well as creates a connection
    with the MongoDB database.
    """
    logging.basicConfig(filename="patient_record_server.log",
                        level=logging.DEBUG)
    print("Connecting to MongoDB...")
    connect("mongodb+srv://pdijour:bme547mongo@bme547.ba348.mongodb.net/"
            "final_project?retryWrites=true&w=majority")
    print("Connection attempt finished.")


@app.route("/", methods=["GET"])
def status():
    """Used to indicate that the server is running
    """
    return "Server is on"


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    in_data = request.get_json()
    error_string, status_code = \
        validate_input(in_data, expected_input)
    if error_string is not True:
        return error_string, status_code
    add_database_entry(in_data["patient_name"],
                       in_data["record_number"],
                       in_data["medical_image_file"],
                       in_data["ECG_image_file"],
                       in_data["heartrate"],
                       in_data["datetime"])
    logging.info("Added new patient into database with id: {}"
                 .format(in_data["record_number"]))
    return "Added patient {}".format(in_data)


expected_input = {"patient_name": str,
                  "record_number": int,
                  "medical_image_file": str,
                  "ECG_image_file": str,
                  "heartrate": int,
                  "datetime": str}


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
    for key in expected_input:
        if key not in in_data:
            return "The key {} is missing from input".format(key), 400
        if expected_input[key] == int:
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


def add_database_entry(patient_name, id_no, medical_files,
                       ecg_files, bpms, timestamps):
    patient_to_add = Patient(name=patient_name,
                             medical_record_number=id_no,
                             medical_images=medical_files,
                             ecg_images=ecg_files,
                             heart_rates=bpms,
                             datetimes=timestamps)
    answer = patient_to_add.save()
    return answer


def find_patient(id_no):
    try:
        patient = Patient.objects.raw({"_id": id_no}).first()
    except pymodm.errors.DoesNotExist:
        patient = False
    return patient


if __name__ == '__main__':
    initialize_server()
    app.run(host="0.0.0.0", port=5001)
