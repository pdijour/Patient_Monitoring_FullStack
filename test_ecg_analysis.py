# test_ecg_analysis.py

import pytest
from math import sqrt
from ecg_analysis import read, filter
from testfixtures import LogCapture

t_normal = [0.1, 12.1, 24.1, 36.1, 48.1, 60.1]
v_normal = [0.2, 120.4, 299.5, 150.1, 130.6, 200.2]
t_missingt = [0.1, 24.1, 36.1, 48.1, 60.1]
v_missingt = [0.2, 299.5, 150.1, 130.6, 200.2]
t_nant = [0.1, 12.1, 24.1, 36.1, 60.1]
v_nant = [0.2, 120.4, 299.5, 150.1, 200.2]
t_missingv = [0.1, 12.1, 36.1, 48.1, 60.1]
v_missingv = [0.2, 120.4, 150.1, 130.6, 200.2]
t_nanv = [0.1, 12.1, 24.1, 48.1, 60.1]
v_nanv = [0.2, 120.4, 299.5, 130.6, 200.2]
v_300 = [0.2, 350.4, 299.5, 306.4, 200.2]
v_neg300 = [0.2, -350.4, 299.5, -306.3, 200.2]


@pytest.mark.parametrize("filename, expected", [
                         ("test_normal.csv", (t_normal, v_normal)),
                         ("test_missingt.csv", (t_missingt, v_missingt)),
                         ("test_nant.csv", (t_nant, v_nant)),
                         ("test_missingv.csv", (t_missingv, v_missingv)),
                         ("test_nanv.csv", (t_nanv, v_nanv))
                         ])
def test_read(filename, expected):
    from ecg_analysis import read
    answer = read(filename)
    assert answer == expected


@pytest.mark.parametrize("filename, expected", [
                         ("test_data/test_data1.csv"),
                         ("test_data/test_nant.csv"),
                         ("test_data/test_missingv.csv"),
                         ("test_data/test_nanv.csv"),
                         ("test_data/test_data11.csv"),
                         ("test_data/test_data20.csv"),
                         ("test_data/test_data28.csv"),
                         ("test_data/test_data31.csv")
                         ])
def test_read(filename):
    from ecg_analysis import read
    with LogCapture() as log_c:
        read(filename)
    log_c.check(("root", "ERROR", "Missing data"))


@pytest.mark.parametrize("filename", [
                         ("test_data/test_data1.csv")
                         ])
def test_read(filename):
    from ecg_analysis import read
    with LogCapture() as log_c:
        read(filename)
    log_c.check()


time_clean, voltage_clean = read("test_data/raw_data1.csv")
time_noise, voltage_noise = read("test_data/test_data1.csv")


@pytest.mark.parametrize("vc, tn, vn", [
                         (voltage_clean,
                          time_noise, voltage_noise)
                         ])
def test_filter(vc, tn, vn):
    sum_f = 0
    sum_n = 0
    sum_c = 0
    from ecg_analysis import filter
    answer = filter(tn, vn)
    for i in answer:
        sum_f += i**2
    rms_f = sqrt(sum_f/len(answer))
    for i in vc:
        sum_c += i**2
    rms_c = sqrt(sum_c/len(answer))
    for i in vn:
        sum_n += i**2
    rms_n = sqrt(sum_n/len(answer))
    print(rms_f)
    print(rms_n)
    assert 4 * rms_f < rms_n
    assert abs(rms_f - rms_c) < 0.5


@pytest.mark.parametrize("voltage", [
                         (v_300), (v_neg300)
                         ])
def test_exceptions(voltage):
    from ecg_analysis import exceptions
    with LogCapture() as log_c:
        exceptions(voltage)
    log_c.check(("root", "WARNING", "Voltage exceeded normal range"))


@pytest.mark.parametrize("voltage", [
                         (v_normal)
                         ])
def test_not_exceptions(voltage):
    from ecg_analysis import exceptions
    with LogCapture() as log_c:
        exceptions(voltage)
    log_c.check()


@pytest.mark.parametrize("time, expected", [
                         (t_normal, 60),
                         (time_noise, 27.775)
                         ])
def test_duration_calc(time, expected):
    from ecg_analysis import duration_calc
    answer = duration_calc(time)
    assert answer == expected


@pytest.mark.parametrize("voltage, expected", [
                         (v_normal, (0.2, 299.5))
                         ])
def test_extremes(voltage, expected):
    from ecg_analysis import extremes
    answer = extremes(voltage)
    assert answer == expected


time_peaks = [0.214, 1.025, 1.839, 2.631, 3.419, 4.206,
              5.025, 5.678, 6.672, 7.517, 8.325, 9.119,
              9.889, 10.731, 11.586, 12.406, 13.236,
              14.056, 14.853, 15.653, 16.439, 17.261,
              18.131, 18.953, 19.739, 20.536, 21.306,
              22.089, 22.906, 23.719, 24.55, 25.392,
              26.2, 26.972]


time_data1, voltage_data1 = read("test_data/test_data1.csv")
voltage_clean1 = filter(time_data1, voltage_data1)
filename = "anything.csv"


@pytest.mark.parametrize("filename, time, voltage, plot, time_peaks", [
                          (filename, time_data1, voltage_clean1, "",
                           time_peaks)
                         ])
def test_show_peaks(filename, time, voltage, plot, time_peaks):
    from ecg_analysis import show_peaks
    answer = show_peaks(filename, time, voltage, "")
    assert answer == time_peaks


@pytest.mark.parametrize("time_peaks, expected", [
                         (time_peaks, 34)
                         ])
def test_num_peaks(time_peaks, expected):
    from ecg_analysis import num_peaks
    answer = num_peaks(time_peaks)
    assert answer == expected


@pytest.mark.parametrize("duration, num_beats, expected", [
                         (27.775, 34, 73)
                         ])
def test_bpm_calc(duration, num_beats, expected):
    from ecg_analysis import bpm_calc
    answer = bpm_calc(duration, num_beats)
    assert answer == expected
