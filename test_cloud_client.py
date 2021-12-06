# test_cloud_client.py

import pytest
from datetime import datetime
from testfixtures import LogCapture
from cloud_server import initialize_server, add_database_entry
from database_definitions import Patient
import io
import os

initialize_server()

pathname = os.getcwd()
full_pathname = pathname + '/images/test_image.jpg'


def convert_file_to_b64_string():
    from cloud_client import convert_file_to_b64_string
    b64str = convert_file_to_b64_string(full_pathname)
    assert b64str[0:20] == "/9j/4AAQSkZJRgABAQEA"


def test_b64_to_ndarray():
    from cloud_client import convert_file_to_b64_string
    from cloud_client import b64_to_ndarray
    b64str = convert_file_to_b64_string("test_image.jpg")
    nd = b64_to_ndarray(b64str)
    answer = nd[0][0:5]
    expected = [[68, 115, 197],
                [68, 115, 197],
                [68, 115, 197],
                [68, 115, 197],
                [68, 115, 197]]
    assert (answer == expected).all


list1 = ['a', 'b', 'c', 'd']
list2 = [23, 98, 47, 24]


@pytest.mark.parametrize("listvar, val, expected", [(list1, 'c', 2),
                                                    (list2, 98, 1)])
def test_get_index(listvar, val, expected):
    from cloud_client import get_index
    answer = get_index(listvar, val)
    assert answer == expected


def test_resize_image():
    from cloud_client import convert_file_to_b64_string
    from cloud_client import b64_to_ndarray
    from cloud_client import resize_image
    b64str = convert_file_to_b64_string("test_image.jpg")
    nd = b64_to_ndarray(b64str)
    resized_nd = resize_image(nd)
    answer = resized_nd[0][0:5]
    expected = [[68, 115, 197],
                [68, 115, 197],
                [68, 115, 197],
                [68, 115, 197],
                [68, 115, 197]]
    assert (answer == expected).all


def test_b64_string_to_file():
    from cloud_client import convert_file_to_b64_string
    from cloud_client import b64_string_to_file
    import filecmp
    import os
    b64str = convert_file_to_b64_string("test_image.jpg")
    b64_string_to_file(b64str, open("test_image_output.jpg", "wb"))
    answer = filecmp.cmp("test_image.jpg",
                         "test_image_output.jpg")
    os.remove("test_image_output.jpg")
    assert answer is True


def test_process_b64():
    from cloud_client import convert_file_to_b64_string
    from cloud_client import b64_to_ndarray
    from cloud_client import resize_image
    b64str = convert_file_to_b64_string("test_image.jpg")
    nd = b64_to_ndarray(b64str)
    resized_nd = resize_image(nd)
    answer = resized_nd[0][0:5]
    expected = [[68, 115, 197],
                [68, 115, 197],
                [68, 115, 197],
                [68, 115, 197],
                [68, 115, 197]]
    assert (answer == expected).all
