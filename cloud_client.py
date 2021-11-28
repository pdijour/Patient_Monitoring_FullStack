# cloud_client.py

import requests

server = "http://127.0.0.1:5000"


def add_patient_to_server(patient_name, id_no, medical_files,
                          ecg_files, bpms, timestamps):
    """ Makes request to server to add specified patient information
    """
    patient1 = {"name": patient_name,
                "medical_record_number": convert_id_to_int(id_no),
                "medical_images": medical_files,
                "ecg_images": ecg_files,
                "heartrate": bpms,
                "datetimes": timestamps}
    r = requests.post(server + "/new_patient", json=patient1)
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


if __name__ == '__main__':
    main()
