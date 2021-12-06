# cloud_client.py

import requests
import requests
import base64

server = "http://127.0.0.1:5000"


def add_files_to_server(patient_name, id_no, medical_files,
                        medical_files_b64, ecg_files, ecg_files_b64,
                        bpms, timestamps):
    """Makes post request to server to add patient information

       This function takes patient information as parameter inputs and makes
       a post request to the database server to store the information. It
       prints the server response to the console as well as returns it to the
       caller.

       Parameters
        ----------
        patient_name : Str
            Contains the patient's name
        id_no : int
            Contains the patient's medical record / ID number
        medical_files : Str
            Contains the file name of the medical image
        medical_files_b64 : Str
            Contains the b64 string of the medical image
        ecg_files : Str
            Contains the file name of the ecg image
        ecg_files_b64 : Str
            Contains the b64 string of the ecg image
        bpms : int
            Contains the heart rate for the chosen ecg file
        timestamps : Str
            Contains the date and time that the heart rate was determined

       Returns
       -------
        r.text
            Containing the server response to the post request
       """
    patient1 = {"patient_name": patient_name,
                "record_number": id_no,
                "medical_image_files": medical_files,
                "medical_images_b64": medical_files_b64,
                "ECG_image_files": ecg_files,
                "ECG_images_b64": ecg_files_b64,
                "heartrates": bpms,
                "datetimes": timestamps}
    r = requests.post(server + "/api/add_files", json=patient1)
    print(r.status_code)
    print(r.text)
    return r.text


def convert_file_to_b64_string(filename):
    """Converts image to b64 string

       This function opens the chosen filename and uses the base64.b64encode
       method to convert the file to a b64 string. If a filename that does not
       exist is entered, the function implement an exception within a try
       except block to return "no file." Otherwise, it returns the b64 string.

       Parameters
        ----------
        filename : Str
            Contains the name of the image file

       Returns
       -------
        String
            Containing the b64 string for the specified image file
       """
    try:
        with open(filename, "rb") as image_file:
            b64_bytes = base64.b64encode(image_file.read())
        b64_string = str(b64_bytes, encoding='utf-8')
    except FileNotFoundError:
        return "no file"
    return b64_string


def main():
    # Check if server running
    r = requests.get(server + "/")
    print(r.status_code)
    print(r.text)

    # Add patient with full data
    add_files_to_server("Yume Choi", 5, "y1.png", "abc", "y2.png", "abc",
                        86, "2020-03-09 11:00:36")

    # Add patient with full data, Strings intead of Ints
    add_files_to_server("Phoebe Dijour", "1", "p1.png", "abc", "p2.png",
                        "abc", "90", "2021-04-15 16:12:23")

    # Add patient with partial data (just ID)
    add_files_to_server("", "10", "", "", "", "", "", "")

    # Add patient with partial data (name and ID)
    add_files_to_server("Rachel Lopez", "11", "", "", "", "", "", "")

    # Add patient with partial data (medical image)
    add_files_to_server("", 2, "m1.png", "abc", "", "", "",
                        "")

    # Add patient with partial data (name, ecg image)
    add_files_to_server("Michael Tian", 3, "", "", "t2.png", "abc",
                        90, "2018-10-25 09:25:20")

    # Check for no medical record number added
    add_files_to_server("Sarah Yu", "", "s1.png", "abc", "s2.png",
                        "abc", 80, "2019-02-22 22:12:22")

    # Check for bad data type
    add_files_to_server("Sarah Yu", "a", "s1.png", "abc", "s2.png",
                        "abc", 80, "2019-02-22 22:12:22")

    # Check for bad data type
    add_files_to_server("Sarah Yu", 7, 3, "abc", "s2.png", "abc", 80,
                        "2019-02-22 22:12:22")

    # Add data for existing patient with full data
    add_files_to_server("Yume Choi", 5, "y3.png", "abc", "y4.png", "abc",
                        98, "2021-10-06 11:11:40")

    # Add data for existing patient with partial data (only medical image)
    add_files_to_server("Meghan Doyle", 2, "m2.png", "abc", "m3.png", "abc",
                        60, "2019-10-12 12:12:40")

    # Add data for existing patient with partial data (name, ecg image)
    add_files_to_server("", 3, "t3.png", "abc", "t4.png", "abc", 60,
                        "2021-11-13 08:09:10")

    # Add partial data for existing patient with full data
    add_files_to_server("", 5, "", "", "y6.png", "abc", 98,
                        "2021-11-08 11:29:59")

    # New name entered for existing patient ID
    add_files_to_server("Youme Choi", 5, "y7.png", "abc", "y8.png", "abc",
                        98, "2021-12-03 04:09:32")

    r = requests.get(server + "/api/record_numbers")
    print(r.text)

    r = requests.post(server + "/api/get_info", json=3)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    main()
