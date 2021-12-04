# cloud_client.py

import requests
import base64

server = "http://127.0.0.1:5000"


def add_files_to_server(patient_name, id_no, medical_files,
                        ecg_files, bpms, timestamps):
    """ Makes request to server to add specified patient information
    """
    id_no = id_no
    patient1 = {"patient_name": patient_name,
                "record_number": id_no,
                "medical_image_files": medical_files,
                "ECG_image_files": ecg_files,
                "heartrates": bpms,
                "datetimes": timestamps}
    r = requests.post(server + "/api/add_files", json=patient1)
    print(r.status_code)
    print(r.text)
    return r.text


def send_image_to_server(filename):
    b64_string = convert_image_file_to_b64_string(filename)
    reply = send_b64_string_to_server(b64_string, filename)
    return reply


def convert_image_file_to_b64_string(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string, filename


def send_b64_string_to_server(b64_string, filename):
    out_json = {"image": b64_string,
                "filename": filename}
    r = requests.post(server + "/api/add_image",
                      json=out_json)
    if r.status_code != 200:
        print(r.text)
        return False
    else:
        print(r.status_code)
        print(r.text)
        return r.text


def main():
    # Check if server running
    r = requests.get(server + "/")
    print(r.status_code)
    print(r.text)

    # Add patient with full data
    add_files_to_server("Yume Choi", 5, "y1.png", "y2.png", 86,
                        "2020-03-09 11:00:36")
    
    # Add patient with full data, Strings intead of Ints
    add_files_to_server("Phoebe Dijour", "1", "p1.png", "p2.png", "90",
                        "2021-04-15 16:12:23")
    
    # Add patient with partial data (medical image)
    add_files_to_server("", 2, "m1.png", "", "",
                        "")
    
    # Add patient with partial data (name, ecg image)
    add_files_to_server("Michael Tian", 3, "", "t2.png", 90,
                        "2018-10-25 09:25:20")
    
    # Check for missing key
    
    # Check for no medical record number added
    add_files_to_server("Sarah Yu", "", "s1.png", "s2.png", 80,
                        "2019-02-22 22:12:22")
    
    # Check for bad data type
    add_files_to_server("Sarah Yu", "a", "s1.png", "s2.png", 80,
                        "2019-02-22 22:12:22")
    
    # Check for bad data type
    add_files_to_server("Sarah Yu", 7, 3, "s2.png", 80,
                        "2019-02-22 22:12:22")
    
    # Add data for existing patient with full data
    add_files_to_server("Yume Choi", 5, "y3.png", "y4.png", 98,
                        "2021-10-06 11:11:40")
    
    # Add data for existing patient with partial data (only medical image)
    add_files_to_server("Meghan Doyle", 2, "m2.png", "m3.png", 60,
                        "2019-10-12 12:12:40")
    
    # Add data for existing patient with partial data (name, ecg image)
    add_files_to_server("", 3, "t3.png", "t4.png", 60,
                        "2021-11-13 08:09:10")
    
    # Add partial data for existing patient with full data
    add_files_to_server("", 5, "", "y6.png", 98,
                        "2021-10-06 11:11:40")
    
    # New name entered for existing patient ID
    add_files_to_server("Youme Choi", 5, "y7.png", "y8.png", 98,
                        "2021-10-06 11:11:40")
    
    # ECG Image uploaded
    send_image_to_server("images/acl1.jpg")

    # r = requests.get(server + "/api/record_numbers")
    # print(r.text)

    # r = requests.post(server + "/api/get_info", json=3)
    # print(r.status_code)
    # print(r.text)


if __name__ == '__main__':
    main()
