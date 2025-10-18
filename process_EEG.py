import numpy as np

def process_eeg_data(eeg_data):
    # Apply filters and extract features
    DataFilter.perform_bandpass(eeg_data, BoardShim.get_sampling_rate(22), 0.5, 50.0, 4, FilterTypes.BUTTERWORTH.value, 0)
    
    # Compute power in specific bands (e.g., alpha, beta)
    alpha_power = DataFilter.get_band_power(eeg_data, 8.0, 13.0)
    beta_power = DataFilter.get_band_power(eeg_data, 13.0, 30.0)
    
    # Simple threshold-based decision
    if alpha_power > beta_power:  # Example condition
        return 'on'
    else:
        return 'off'

while True:
    data = board.get_board_data()
    eeg_data = data[1:5, :]  # Channels 1 to 4 for EEG data

    decision = process_eeg_data(eeg_data)
    print(f"Decision: {decision}")
