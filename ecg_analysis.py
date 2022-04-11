import pandas as pd
import logging
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import json


def input_csv(filepath):
    """Read csv file and convert to two list of floats

    Read csv file, remove all NaN and non-numerical values, return
    clean lists of time and voltage. log an error to the log file
    if there is data missing or non-numerical values.

    Args:
        filepath (string): the filepath and name of the csv file

    Returns:
        list: a list of floats containing all of the timepoints
        list: a list of floats containing all of the voltage
    """
    logging.info("Starting analysis of a new ECG trace: " + filepath)
    data = pd.read_csv(filepath,  header=None)
    # converting column data to list
    time_raw = data[0].tolist()
    voltage_raw = data[1].tolist()
    time = []
    voltage = []
    for i in range(len(time_raw)):
        try:
            # Try to convert to float
            timepoint = float(time_raw[i])
            voltagepoint = float(voltage_raw[i])
            if (math.isnan(timepoint)) or (math.isnan(voltagepoint)):
                # Do not append if there is nan, display warning
                logging.error(
                    "pair contains a missing value or NaN in line {}"
                    .format(i+1))
            else:
                time.append(timepoint)
                voltage.append(voltagepoint)
        except ValueError:
            # Do not append if there is a non-numetric string
            # (couldn't convert to float error), display warning
            logging.error(
                "pair contains a non-numeric string in line {}".format(i+1))
    if any(abs(i) >= 300 for i in voltage):
        logging.warning("Voltages exceeded the normal range in: " + filepath)

    return time, voltage


def get_duration(time):
    """Get duration according to the time list

    Get duration of the time according to the start and end of the time

    Args:
        time (list): a list of floats containing all of the timepoints

    Returns:
        float: time duration of the ECG strip as a numeric value
    """
    logging.info("Start calculation of duration")
    duration = time[-1] - time[0]

    return duration


def get_voltage_extremes(voltage):
    """Get duration according to the time list

    Get duration of the time according to the start and end of the time

    Args:
        voltage (list): a list of floats containing all of the voltage

    Returns:
        tuple: tuple in the form (min, max) where min and max are the
            minimum and maximum lead voltages as found in the raw data file
    """
    logging.info("Start calculation of voltage_extremes")
    min_voltage = min(voltage)
    max_voltage = max(voltage)
    voltage_extremes = (min_voltage, max_voltage)

    return voltage_extremes


def butter_bandpass_filter(time, voltage):
    """filter the data with butterworh bandpassfilter

    Use Butterworth filter function imported from scipy to filter the data.
    Normal bpm is within 60-100 beats/min, and the data has
    additional low (<1 Hz) and/or high (>50 Hz) frequency noise.
    To read more about butterworh filter in scipy, please refer to:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html

    Args:
        time(list): a list of floats containing all of the timepoints
        voltage (list): a list of floats containing all of the voltage

    Returns:
        list: a list of floats containing all of the voltage
            after bandpass filtering
    """
    logging.info("Start filtering the data")
    lowcut = 1  # unit: Hz
    highcut = 50  # unit: Hz
    fs = 1/(time[1] - time[0])
    wn1 = 2 * lowcut / fs
    wn2 = 2 * highcut / fs
    b, a = signal.butter(5, [wn1, wn2], 'bandpass', output='ba')
    # b1, a1 = signal.butter(5, wn2, 'lowpass', output='ba')
    # b2, a2 = signal.butter(5, wn1, 'highpass', output='ba')
    voltage_filtered = signal.filtfilt(b, a, voltage, padtype='even')

    return voltage_filtered


def find_beats(time, voltage_filtered):
    """find the beats by finding peaks in voltage data

    This function finds the beats by looking for local peaks.
    It calls scipy.signal.find_peaks that finds all local maxima
    by simple comparison of neighboring values.
    For more infomation about how the scipy.signal.find_peaks works,
    please refer to:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html

    Args:
        time(list): a list of floats containing all of the timepoints
        voltage_filtered (list): a list of floats containing all of the voltage
            after bandpass filtering

    Returns:
        list: a list of floats of times when a beat occurred
    """
    logging.info("Start calculation of beats")
    dt = time[1] - time[0]
    if max(voltage_filtered[100:-100]) <= 1.5:
        # Avoid shoulder effect
        threshold = 0.68 * max(voltage_filtered[100:-100])
    else:
        threshold = 0.7
    dist = int(1/5/dt)  # heart beat frequency should < 5
    peaks, _ = signal.find_peaks(voltage_filtered, threshold, distance=dist)
    # Convert to array, to use list as index. (peaks is indices list)
    time = np.array(time)
    voltage_filtered = np.array(voltage_filtered)
    beats_arr = time[peaks]
    beats = beats_arr.tolist()
    # plt.plot(time, voltage_filtered)
    # plt.plot(time[peaks], voltage_filtered[peaks], "x")
    # plt.show()

    return beats


def get_num_beats(beats):
    """find the number of beats according to the given beats list

    This function calculates the number of beats according to the length
    of the given beats list

    Args:
        beats(list): a list of floats of times when a beat occurred

    Returns:
        int: number of detected beats in the strip
    """
    logging.info("Start calculation of num_beats")
    num_beats = len(beats)

    return num_beats


def get_mean_hr_bpm(duration, num_beats):
    """Calculate the mean_hr_bpm according to duration and number of beats

    This function calculates estimated average heart rate over the
    duration of the ECG strip. mean_hr_bpm has the unit heart beats per second

    Args:
        duration(float): time duration of the ECG strip as a numeric value
        num_beats(int): number of detected beats in the strip

    Returns:
        float: estimated average heart rate over the length of the strip.
            unit: heart beats per minute.
    """
    logging.info("Start calculation of mean_hr_bpm")
    mean_hr_bpm = num_beats/(duration/60)  # convert unit to per minute

    return mean_hr_bpm


def convert2dict(duration, voltage_extremes, num_beats, mean_hr_bpm, beats):
    """Covert all  calculated data into a Python dictionary called metrics

    Take all the data calculated before and save them as keys in a Python
    dictionary called metrics.

    Args:
        duration(float): time duration of the ECG strip as a numeric value
        voltage_extremes(tuple): tuple in the form (min, max) where min and
            max are the minimum and maximum lead voltages as found
            in the raw data file
        num_beats(int): number of detected beats in the strip
        mean_hr_bpm(float): estimated average heart rate over the
            length of the strip. unit: heart beats per minute.
        beats(list):  a list of floats of times when a beat occurred

    Returns:
        dictionary: a dictionary that contains all the metrics data including
            duration, voltage_extremes, num_beats, mean_hr_bpm, beats.
    """
    logging.info("Start generating the dictionary")
    metrics = {
        "duration": duration,
        "voltage_extremes": voltage_extremes,
        "num_beats": num_beats,
        "mean_hr_bpm": mean_hr_bpm,
        "beats": beats,
    }
    return metrics


def get_json_name(filepath):
    """Get name of the output json according to data file name

    Get name of the output json file according to the original csv
    file name.

    Args:
        filepath (string): the filepath and name of the csv file

    Returns:
        string: name of the output json file containg the name information
            of the input data
    """
    logging.info("Generating name for the json output")
    json_name = filepath[10:-4] + ".json"

    return json_name


def ouput_json(json_name, metrics):
    """Output json file

    Output file that contains a dictionary of the metrics
    in JSON format

    Args:
        json_name (string): name of the output json file
        metrics (dictionary): a dictionary that contains all the
            metrics data including duration, voltage_extremes,
            num_beats, mean_hr_bpm, beats.
    """
    with open(json_name, "w") as out_file:
        json.dump(metrics, out_file)


def main():
    """main function for ecg analysis

    main function for ecg analysis that calls all the function,
    output the json file as the same file name with the json format

    Args:
        json_name (string): name of the output json file
        metrics (dictionary): a dictionary that contains all the
            metrics data including duration, voltage_extremes,
            num_beats, mean_hr_bpm, beats.
    """
    logging.basicConfig(filename="log_example.log",
                        filemode="w", level=logging.INFO)
    filepath = "test_data/test_data23.csv"  # 5, 7, 11, 23
    time, voltage = input_csv(filepath)
    duration = get_duration(time)
    voltage_extremes = get_voltage_extremes(voltage)
    # plt.plot(time, voltage)
    # plt.show()
    voltage_filtered = butter_bandpass_filter(time, voltage)
    # plt.plot(time, voltage_filtered)
    # plt.show()
    beats = find_beats(time, voltage_filtered)
    num_beats = get_num_beats(beats)
    mean_hr_bpm = get_mean_hr_bpm(duration, num_beats)
    metrics = convert2dict(
        duration, voltage_extremes, num_beats, mean_hr_bpm, beats)
    json_name = get_json_name(filepath)
    ouput_json(json_name, metrics)


def analyze_ecg(filepath):
    """Do ECG data analysis for patient-side client

    Calculate heart rate and generate filered voltage plot for the
    input data for patient-side client.

    Args:
        filepath (string): the filepath and name of the csv file

    Returns:
        int: average heart rate of ECG data
        string: the filepath and name of the output voltage image
    """
    time, voltage = input_csv(filepath)
    duration = get_duration(time)
    voltage_filtered = butter_bandpass_filter(time, voltage)
    beats = find_beats(time, voltage_filtered)
    num_beats = get_num_beats(beats)
    mean_hr_bpm = get_mean_hr_bpm(duration, num_beats)
    plt.figure(figsize=(12, 6))
    plt.plot(time, voltage_filtered)
    plt.xlabel('time(s)')
    plt.ylabel('voltage(mv)')
    file = filepath.split('/')[-1].split('.')[0]
    savepath = 'ecg_images/' + file + '.jpg'
    plt.savefig(savepath)
    plt.close()
    return int(mean_hr_bpm), savepath


if __name__ == "__main__":
    main()
