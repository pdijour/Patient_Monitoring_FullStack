# test_cloud_server.py

import pytest
from datetime import datetime
from testfixtures import LogCapture
from cloud_server import initialize_server

initialize_server()


err_str_1 = "The value corresponding to the key patient_id " \
            "is not an integer."
err_str_2 = "The value corresponding to the key patient_age " \
            "is not an integer."


@pytest.mark.parametrize("in_data, key, expected",
                         [({"patient_id": 25,
                            "attending_username": "Pan.M",
                            "patient_age": 54}, "patient_id",
                           {"patient_id": 25,
                            "attending_username": "Pan.M",
                            "patient_age": 54}),
                          ({"patient_id": "13",
                            "attending_username": "Pan.T",
                            "patient_age": 54}, "patient_id",
                           {"patient_id": 13,
                            "attending_username": "Pan.T",
                            "patient_age": 54}),
                          ({"patient_id": "abc",
                            "attending_username": "Tian.J",
                            "patient_age": 54}, "patient_id",
                           err_str_1),
                          ({"patient_id": "34c",
                            "attending_username": "Choi.Y",
                            "patient_age": 54}, "patient_id",
                           err_str_1),
                          ({"patient_id": "34c",
                            "attending_username": "Zhang.C",
                            "patient_age": 54}, "patient_age",
                           {"patient_id": "34c",
                            "attending_username": "Zhang.C",
                            "patient_age": 54}),
                          ({"patient_id": "57",
                            "attending_username": "Punia.V",
                            "patient_age": "54a"}, "patient_age",
                           err_str_2),
                          ({"patient_id": "23adb",
                            "attending_username": "Kim.N",
                            "patient_age": "54"}, "patient_age",
                           {"patient_id": "23adb",
                            "attending_username": "Kim.N",
                            "patient_age": 54})])
def test_check_int(in_data, key, expected):
    from cloud_server import check_int
    result = check_int(in_data, key)
    assert result == expected


err_str_3 = "The input was not a dictionary."
err_str_4 = "The key patient_id is missing from input"
err_str_5 = "The key patient_age is missing from input"
err_str_6 = "The key attending_username is missing from input"
err_str_13 = "The key attending_username is missing from input"
err_str_14 = "The key attending_email is missing from input"
err_str_15 = "The key attending_phone is missing from input"
err_str_17 = "The key patient_id is missing from input"
err_str_18 = "The key heart_rate is missing from input"
err_str_20 = "The key patient_id is missing from input"
err_str_21 = "The key heart_rate_average_since is missing from input"
expected_patient_input = {"patient_id": int,
                          "attending_username": str,
                          "patient_age": int}
expected_attending_input = {"attending_username": str,
                            "attending_email": str,
                            "attending_phone": str}
expected_hr_input = {"patient_id": int,
                     "heart_rate": int}
expected_interval_input = {"patient_id": int,
                           "heart_rate_average_since": str}


@pytest.mark.parametrize("in_data, expected_input, expected_val, "
                         "expected_code",
                         [({"patient_id": 25,
                            "attending_username": "Fisher.B",
                            "patient_age": 45555},
                           expected_patient_input, True, 200),
                          ({"patient_ids": "234",
                            "attending_username": "Pan.M",
                            "patient_age": "43"},
                           expected_patient_input, err_str_4, 400),
                          ({"patient_id": 67,
                            "Doctor": "Choi.Y",
                            "patient_age": 45},
                           expected_patient_input, err_str_6, 400),
                          ({"patient_id": "98",
                            "attending_username": "Punia.V",
                            "Age in years": 54,
                            "Fun facts": []},
                           expected_patient_input, err_str_5, 400),
                          ({"patient_num": 243,
                            "doc": "Zhang.C"},
                           expected_patient_input, err_str_4, 400),
                          ("in_data",  expected_patient_input, err_str_3, 400),
                          (54, expected_patient_input, err_str_3, 400),
                          ({}, expected_patient_input, err_str_4, 400),
                          ({"attending_username": "Pan.M",
                            "attending_email": "mpan@gmail.com",
                            "attending_phone": "732-320-5855"},
                           expected_attending_input, True, 200),
                          ({"attending_name": "Pan.M",
                            "attending_email": "mpan@gmail.com",
                            "attending_phone": "732-320-5855"},
                           expected_attending_input,
                           err_str_13, 400),
                          ({"attending_username": "Pan.M",
                            "send_here": "mpan@gmail.com",
                            "attending_phone": "732-320-5855"},
                           expected_attending_input,
                           err_str_14, 400),
                          ({"attending_username": "Pan.M",
                            "attending_email": "mpan@gmail.com",
                            "call_here": "732-320-5855"},
                           expected_attending_input, err_str_15, 400),
                          ({"name_doc": "Pan.M",
                            "attending_email": "mpan@gmail.com"},
                           expected_attending_input,
                           err_str_13, 400),
                          ("in_data", expected_attending_input,
                           err_str_3, 400),
                          (54, expected_attending_input, err_str_3, 400),
                          ({}, expected_attending_input, err_str_13, 400),
                          ({"patient_id": 25,
                            "heart_rate": 96}, expected_hr_input, True, 200),
                          ({"patient_id": "25",
                            "heart_rate": "96"}, expected_hr_input, True, 200),
                          ({"patient_ids": "234",
                            "heart_rate": 86}, expected_hr_input,
                           err_str_17, 400),
                          ({"patient_id": 67,
                            "bpm": "89"}, expected_hr_input, err_str_18, 400),
                          ("in_data", expected_hr_input, err_str_3, 400),
                          (54, expected_hr_input, err_str_3, 400),
                          ({}, expected_hr_input, err_str_4, 400),
                          ({"patient_id": 25,
                            "heart_rate_average_since": "2020-03-09 11:00:36"},
                           expected_interval_input, True, 200),
                          ({"patient_id": 25,
                            "heart_rate_average_since": "2020-03-09 11:00:36"},
                           expected_interval_input, True, 200),
                          ({"patient_ids": "234",
                            "heart_rate_average_since": "2020-03-09 11:00:36"},
                           expected_interval_input, err_str_20, 400),
                          ({"patient_id": 67,
                            "since": "2020-03-09 11:00:36"},
                           expected_interval_input, err_str_21, 400),
                          ("in_data", expected_interval_input, err_str_3, 400),
                          (54, expected_interval_input, err_str_3, 400),
                          ({}, expected_interval_input, err_str_4, 400)])
def test_validate_input(in_data, expected_input, expected_val, expected_code):
    from cloud_server import validate_input
    result = validate_input(in_data, expected_input)
    assert result == (expected_val, expected_code)


def test_add_database_entry():
    from cloud_server import add_database_entry
    expected_name = "David Testing"
    answer = add_database_entry(expected_name, 5, "1.png", "2.png", 86,
                                "2020-03-09 11:00:36")
    answer.delete()
    assert answer.name == expected_name


def test_find_patient():
    from cloud_server import find_patient
    from cloud_server import add_database_entry
    expected_name = "Yume Choi"
    expected_id = 32
    entry_to_delete = add_database_entry(expected_name, expected_id, "1.png",
                                         "2.png", 86, "2020-03-09 11:00:36")
    answer = find_patient(expected_id)
    entry_to_delete.delete()
    assert answer.id == expected_id
    assert answer.name == expected_name


def test_add_database_entry_is_made():
    from cloud_server import add_database_entry
    with LogCapture() as log_c:
        add_database_entry("Choi.Y", 5, "1.png", "2.png", 86,
                           "2020-03-09 11:00:36")
    log_c.check(("root", "INFO", "Added new patient into database with id: 5"))
