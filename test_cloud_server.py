# test_cloud_server.py

import pytest
from datetime import datetime
from testfixtures import LogCapture
from cloud_server import initialize_server, add_database_entry
from database_definitions import Patient

initialize_server()


err_str_1 = "The value corresponding to the key record_number " \
            "is not an integer."


@pytest.mark.parametrize("in_data, key, expected",
                         [({"patient_name": "Yume Choi",
                            "record_number": 3,
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": 90,
                            "datetimes": "2021-10-06 11:11:40"},
                           "record_number",
                           {"patient_name": "Yume Choi",
                            "record_number": 3,
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": 90,
                            "datetimes": "2021-10-06 11:11:40"}),
                          ({"patient_name": "David Tan",
                            "record_number": "3",
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": 90,
                            "datetimes": "2021-10-06 11:11:40"},
                           "record_number",
                           {"patient_name": "David Tan",
                            "record_number": 3,
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": 90,
                            "datetimes": "2021-10-06 11:11:40"}),
                          ({"patient_name": "Matthew Weintraub",
                            "record_number": "a",
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": 90,
                            "datetimes": "2021-10-06 11:11:40"},
                           "record_number", err_str_1)])
def test_check_int(in_data, key, expected):
    from cloud_server import check_int
    result = check_int(in_data, key)
    assert result == expected


err_str_3 = "The input was not a dictionary."
err_str_4 = "The key record_number is empty"
expected_patient_input = {"patient_name": str,
                          "record_number": int,
                          "medical_image_files": str,
                          "medical_images_b64": str,
                          "ECG_image_files": str,
                          "ECG_images_b64": str,
                          "heartrates": int,
                          "datetimes": str}


@pytest.mark.parametrize("in_data, expected_input, expected_val,"
                         "expected_code",
                         [({"patient_name": "Yume Choi",
                            "record_number": 3,
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": 90,
                            "datetimes": "2021-10-06 11:11:40"},
                           expected_patient_input, True, 200),
                          ({"patient_name": "Yume Choi",
                            "record_number": "3",
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": "90",
                            "datetimes": "2021-10-06 11:11:40"},
                           expected_patient_input, True, 200),
                          ({"patient_name": "Yume Choi",
                            "record_number": "",
                            "medical_image_files": "y1.png",
                            "medical_images_b64": "abc123",
                            "ECG_image_files": "y2.png",
                            "ECG_images_b64": "def456",
                            "heartrates": 90,
                            "datetimes": "2021-10-06 11:11:40"},
                           expected_patient_input, err_str_4, 400),
                          (54, expected_patient_input, err_str_3, 400)])
def test_validate_input(in_data, expected_input, expected_val, expected_code):
    from cloud_server import validate_input
    result = validate_input(in_data, expected_input)
    assert result == (expected_val, expected_code)


def test_add_database_entry():
    from cloud_server import add_database_entry
    expected_name = "Yume Choi"
    answer = add_database_entry(expected_name, 5, "1.png", "abc123", "2.png",
                                "def456", 86, "2020-03-09 11:00:36")
    answer.delete()
    assert answer.name == expected_name


def test_find_patient():
    from cloud_server import find_patient
    from cloud_server import add_database_entry
    expected_name = "Yume Choi"
    expected_id = 5
    entry_to_delete = add_database_entry(expected_name, expected_id, "1.png",
                                         "abc123", "2.png", "def456", 86,
                                         "2020-03-09 11:00:36")
    answer = find_patient(expected_id)
    entry_to_delete.delete()
    assert answer.medical_record_number == expected_id
    assert answer.name == expected_name


def test_add_database_entry_is_made():
    from cloud_server import add_database_entry
    with LogCapture() as log_c:
        entry_to_delete = add_database_entry("Yume Choi", 5, "1.png",
                                             "abc123", "2.png", "def456", 86,
                                             "2020-03-09 11:00:36")
        entry_to_delete.delete()
    log_c.check(("root", "INFO", "Added new patient into database with id: 5"))


def test_add_patient_file_is_made():
    from cloud_server import add_patient_file
    with LogCapture() as log_c:
        entry_to_delete = add_database_entry("Yume Choi", 5, "1.png",
                                             "abc123", "2.png", "def456", 86,
                                             "2020-03-09 11:00:36")
        add_patient_file("Yume Choi", 5, "3.png", "abc123", "4.png",
                         "def456", 90, "2021-04-10 12:11:59")
        entry_to_delete.delete()
    log_c.check(("root", "INFO", "Added new patient into database with id: 5"),
                ("root", "INFO", "Added new file for patient with id: 5"))


entry_to_delete1 = add_database_entry("Max Silver", 9, "1.png", "m1", "2.png",
                                      "e2", 86, "2020-03-09 11:00:36")
expected_vals1 = ("Max Silver", 9, ["1.png", "3.png"], ["m1", "m3"],
                  ["2.png", "4.png"], ["e2", "e4"], [86, 90],
                  ["2020-03-09 11:00:36", "2021-04-10 12:11:59"])
entry_to_delete2 = add_database_entry("", 10, "1.png", "m1", "2.png", "e2",
                                      86, "2020-03-09 11:00:36")
expected_vals2 = ("Maria Lopez", 10, ["1.png", "3.png"], ["m1", "m3"],
                  ["2.png", "4.png"], ["e2", "e4"], [86, 90],
                  ["2020-03-09 11:00:36", "2021-04-10 12:11:59"])
entry_to_delete3 = add_database_entry("Martha Ball", 11, "1.png", "m1",
                                      "2.png", "e2", 86, "2020-03-09 11:00:36")
expected_vals3 = ("Martha Ball", 11, ["1.png"], ["m1"], ["2.png", "4.png"],
                  ["e2", "e4"], [86, 90],
                  ["2020-03-09 11:00:36", "2021-04-10 12:11:59"])
entry_to_delete4 = add_database_entry("Martin Zoom", 12, "1.png", "m1",
                                      "2.png", "e2", 86,
                                      "2020-03-09 11:00:36")
expected_vals4 = ("Martin Zoom", 12, ["1.png", "3.png"], ["m1", "m3"],
                  ["2.png"], ["e2"], [86], ["2020-03-09 11:00:36"])


@pytest.mark.parametrize("entry, patient_name, id_no, medical_file,"
                         "medical_b64, ecg_file, ecg_b64, bpm, timestamp,"
                         "expected",
                         [(entry_to_delete1, "Max Silver", 9,
                           "3.png", "m3", "4.png", "e4", 90,
                           "2021-04-10 12:11:59", expected_vals1),
                          (entry_to_delete2, "Maria Lopez", 10,
                           "3.png", "m3", "4.png", "e4", 90,
                           "2021-04-10 12:11:59", expected_vals2),
                          (entry_to_delete3, "Martha Ball", 11,
                           "", "", "4.png", "e4", 90, "2021-04-10 12:11:59",
                           expected_vals3),
                          (entry_to_delete4, "Martin Zoom", 12,
                           "3.png", "m3", "", "", "",  "",
                           expected_vals4)])
def test_add_patient_file(entry, patient_name, id_no, medical_file,
                          medical_b64, ecg_file, ecg_b64, bpm,
                          timestamp, expected):
    from cloud_server import add_patient_file
    answer = add_patient_file(str(patient_name), id_no, medical_file,
                              medical_b64, ecg_file, ecg_b64, bpm, timestamp)
    entry.delete()
    assert (answer.name, answer.medical_record_number,
            answer.medical_images, answer.medical_images_b64,
            answer.ecg_images, answer.ecg_images_b64,
            answer.heart_rates, answer.datetimes) == expected


def test_patient_name_change():
    from cloud_server import add_database_entry
    from cloud_server import add_patient_file
    with LogCapture() as log_c:
        entry_to_delete = add_database_entry("Yume Choi", 3, "1.png", "abc123",
                                             "2.png", "def456", 86,
                                             "2020-03-09 11:00:36")
        add_patient_file("Youme Choi", 3, "3.png", "abc123", "4.png", "abc123",
                         90, "2021-04-10 12:11:59")
        entry_to_delete.delete()
    log_c.check(('root', 'INFO', 'Added new patient into database with id: 3'),
                ('root', 'WARNING', 'Entered patient name does not match '
                 'records for 3. Patient name will now be set to Youme Choi'),
                ('root', 'INFO', 'Added new file for patient with id: 3'))


def test_list_record_numbers():
    from cloud_server import list_record_numbers
    from cloud_server import add_database_entry
    entry = add_database_entry("Yume Choi", 3, "1.png", "m1", "2.png", "e2",
                               86, "2020-03-09 11:00:36")
    entry_2 = add_database_entry("Michael Tian", 5, "1.png", "m1", "2.png",
                                 "e2", 86, "2020-03-09 11:00:36")
    entry_3 = add_database_entry("Phoebe Dij", 11, "1.png", "m1", "2.png",
                                 "e2", 86, "2020-03-09 11:00:36")
    answer = list_record_numbers()
    entry.delete()
    entry_2.delete()
    entry_3.delete()
    expected = [3, 5, 11]
    assert answer == expected


expected_info = {"name": "Yume Choi",
                 "medical_record_number": 3,
                 "medical_images": "acl1.png",
                 "medical_images_b64": "123",
                 "ecg_images": "ecg1.png",
                 "ecg_images_b64": "456",
                 "heart_rates": 85,
                 "datetimes": "2020-03-00 11:00:36"}


def test_retrieve_all_info():
    from cloud_server import retrieve_all_info
    b64_images = ["123", "456", "789"]
    patient1 = Patient("Yume Choi", 3, "acl1.png", b64_images[0], "ecg1.png",
                       b64_images[1], 85, "2020-03-00 11:00:36")
    patient1.save()

    answer = retrieve_all_info(3)
    patient1.delete()
    expected = expected_info
    assert answer == expected
