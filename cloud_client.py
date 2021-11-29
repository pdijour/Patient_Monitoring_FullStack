# cloud_client.py

import requests

server = "http://127.0.0.1:5000"


def add_files_to_server(patient_name, id_no, medical_files,
                        ecg_files, bpms, timestamps):
    """ Makes request to server to add specified patient information
    """
    patient1 = {"patient_name": patient_name,
                "record_number": convert_id_to_int(id_no),
                "medical_image_files": medical_files,
                "ECG_image_files": ecg_files,
                "heartrates": bpms,
                "datetimes": timestamps}
    r = requests.post(server + "/api/add_files", json=patient1)
    print(r.status_code)
    print(r.text)
    return r.text


def convert_id_to_int(id_input):
    id_output = int(id_input)
    return id_output


def main():
    # Check if server running
    r = requests.get(server + "/")
    print(r.status_code)
    print(r.text)

    # Add patient
    add_files_to_server("Yume Choi", 5, "y1.png", "y2.png", 86,
                        "2020-03-09 11:00:36")

    # Add patient
    add_files_to_server("Phoebe Dijour", 2, "p1.png", "p2.png", 90,
                        "2021-04-15 16:12:23")

    # Check for missing key

    # Check for bad data type

    # Add data for existing patient
    add_files_to_server("Yume Choi", 5, "y3.png", "y4.png", 98,
                        "2021-10-06 11:11:40")

    # Check if patient does not exist


if __name__ == '__main__':
    main()
