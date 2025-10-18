from muselsl import list_muses, stream
import numpy as np
from scipy.signal import butter, lfilter
from phue import Bridge

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

def control_light(filtered_data, threshold, bridge, light_name):
    if np.mean(filtered_data) > threshold:
        bridge.set_light(light_name, 'on', True)
    else:
        bridge.set_light(light_name, 'on', False)

# Main script
muses = list_muses()
if not muses:
    print("No MUSE headbands found")
else:
    stream(muses[0]['address'])

    raw_data = []  # Replace with actual data retrieval logic
    fs = 256
    lowcut = 8.0
    highcut = 12.0
    filtered_data = bandpass_filter(raw_data, lowcut, highcut, fs)

    b = Bridge('your_bridge_ip_address')
    alpha_threshold = 100
    control_light(filtered_data, alpha_threshold, b, 'Your Light Name')
