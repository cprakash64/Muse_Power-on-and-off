import numpy as np
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Example usage: filter alpha waves (8-12 Hz)
fs = 256  # Sampling frequency
lowcut = 8.0
highcut = 12.0

filtered_data = bandpass_filter(raw_data, lowcut, highcut, fs)
