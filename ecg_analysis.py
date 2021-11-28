# ecg_analysis.py

import json
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt
import math
import logging
import csv


def read(filename):
    """Open file using csv reader and load variable with data

    This code loads every five lines of the text file into an element of a list
    called patients.

    :param filename: string containing the file name to-be-opened

    :returns: string containing each patient's full data in a separate element
    """
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        time = []
        voltage = []
        for i in reader:
            both = i[0]
            both_list = both.split(',')
            time_val = both_list[0]
            voltage_val = both_list[1]
            try:
                if not math.isnan(float(time_val)) and\
                  not math.isnan(float(voltage_val)):
                    time.append(float(time_val))
                    voltage.append(float(voltage_val))
            except ValueError:
                logging.error("Missing data")
    return time, voltage


def filter(time, voltage):
    """Filter voltage data using bandpass butter filter

    This code filters the 1 Hz and 50 Hz noise in the voltage data using
    a butter filter and the scipy.signal filtfilt function. It uses a third
    order filter and Nyquist sampling frequency to calculate critical
    frequency.

    :param time: list of floats containing all time data points
    :param voltage: list of floats containing all voltage data points

    :returns: list of floats containing filtered voltage values
    """
    fc = [1, 50]
    sampling_rate = len(voltage) / duration_calc(time)
    w = [fc[0] / (sampling_rate / 2), fc[1] / (sampling_rate / 2)]
    b, a = butter(3, w, 'band')
    output = filtfilt(b, a, voltage)
    return output


def exceptions(voltage):
    """Log warning in values are outside the normal range of +/- 300 mV

    This code creates a warning log when the voltage exceeds the normal
    range of values between -300 mV and +300 mV.

    :param voltage: list of floats containing all voltage data points
    """
    for v in voltage:
        if v > 300 or v < -300:
            logging.warning("Voltage exceeded normal range")
            break


def duration_calc(time):
    """Calculate time duration of ECG strip

    This code takes the difference between the first and last time
    points in order to calculate the time duration of the ECG strip.

    :param time: list of floats containing all time data points

    :returns: float containing time duration of ECG strip in seconds
    """
    duration = time[-1] - time[0]
    return duration


def extremes(voltage):
    """Calculate voltage min and max of ECG strip

    This code uses min() and max() functions to calculate the minimum
    and maximum voltages values within one ECG strip.

    :param voltage: list of floats containing all voltage data points

    :returns: float containing minimum voltage value
    :returns: float containing maximum voltage value
    """
    minimum = min(voltage)
    maximum = max(voltage)
    return minimum, maximum


def show_peaks(filename, time, voltage, plot):
    """Plot filtered data with peaks and calculate time and voltage of
    each peak

    This code uses the scipy find_peaks function to determine the time
    location of each peak. Based on all of the test ECG data files,
    it was determined that all peaks are at least 35% of the maximum
    voltage, and peaks are never less than 100 data points away from
    one another. Therefore, these parameters were used in the find_peaks
    function.

    :param filename: string containing file name
    :param time: list of floats containing all time data points
    :param voltage: list of floats containing all filtered voltage data
    points
    :param plot: boolean where TRUE saves the plotted figure and FALSE
    does not

    :returns: list of floats containing times where peaks occured
    """
    filename_png = "{}.png".format(filename.strip(".csv"))
    peaks, _ = find_peaks(voltage, height=max(voltage) * 0.35, distance=100)
    time_peaks = [time[i] for i in peaks]
    if plot == "save":
        plt.figure()
        plt.plot(time, voltage)
        plt.savefig(filename_png)
    return time_peaks


def num_peaks(time_peaks):
    """Calculate the number of peaks in ECG strip

    This code calculates the number of peaks in an ECG strip using
    the length of the lift of voltage peaks, found in the previous show_peaks
    function.

    :param voltage_peaks: list of floats containing voltages of peaks

    :returns: int containing number of peaks
    """
    num_beats = len(time_peaks)
    return num_beats


def bpm_calc(duration, num_beats):
    """Calculate average heartrate within ECG strip

    This code calculates the average beats per minute of an ECG strip
    by dividing the total number of beats by the total amount of time
    in minutes.

    :param duration: float containing time duration of ECG strip in seconds

    :returns: float containing heartrate of ECG strip in bpm
    """
    time_min = duration / 60
    bpm = float("{:.2f}".format(num_beats/time_min))
    return bpm


def create_dict(filename, duration, min, max, num_beats, bpm, time_peaks):
    """Create dictionary of ECG metrics and output to JSON file

    This code creates a dictionary of metrics, including time duration,
    voltage extremes, number of beats, mean heartrate, times of beats. It
    dumps this dictionary into a JSON file that has the same name as the
    ECG data file, but with an extension of .json. It also logs when a
    dictionary entry is assigned.

    :param filename: string containing ECG data file name
    :param duration: float containing time duration of ECG strip
    :param min: float containing minimum voltage value of ECG strip
    :param max: float containing maximum voltage value of ECG strip
    :param num_beats: int containing number of beats in ECG strip
    :param bpm: float containing heartrate of ECG strip in bpm
    :param time_peaks: list of floats containing times where peaks occured
    """
    metrics = {"duration": duration, "voltage_extremes": (min, max),
               "num_beats": num_beats, "mean_hr_bpm": bpm,
               "beats": time_peaks}
    filename = "{}.json".format(filename.strip(".csv"))
    logging.info("Assigning Dictionary Entry")
    with open(filename, 'w') as out_file:
        json.dump(metrics, out_file)


def overall_plotting(filename):
    time, voltage = read(filename)
    voltage_clean = filter(time, voltage)
    show_peaks(filename, time, voltage_clean, "save")


def overall_rate(filename):
    time, voltage = read(filename)
    voltage_clean = filter(time, voltage)
    duration = duration_calc(time)
    time_peaks = show_peaks(filename, time, voltage_clean, "")
    num_beats = num_peaks(time_peaks)
    bpm = bpm_calc(duration, num_beats)
    return "{}".format(bpm)


if __name__ == "__main__":
    """Runs main code and asks for user input

    This code allows the user to input their text file of choice and then runs
    through all of the aforementioned functions in order to create json files
    for each patient in the text file.
    """
    logging.basicConfig(filename="Logging.log",
                        filemode='w', level=logging.INFO)
