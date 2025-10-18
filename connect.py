import time
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations

def main():
    # Initialize board parameters for MUSE
    params = BrainFlowInputParams()
    params.serial_port = ''  # For MUSE, typically this can be left empty
    params.mac_address = 'XX:XX:XX:XX:XX:XX'  # Replace with your MUSE headband's MAC address
    params.ip_address = ''
    params.ip_port = 0
    params.other_info = ''
    params.timeout = 0
    params.file = ''

    # Use BoardIds.MUSE_2_BOARD for MUSE 2 headband
    board_id = BoardIds.MUSE_2_BOARD.value
    board = BoardShim(board_id, params)

    # Enable BrainFlow logging
    BoardShim.enable_dev_board_logger()

    # Debug: Print parameters
    print(f"Board ID: {board_id}")
    print(f"MAC Address: {params.mac_address}")

    # Retry mechanism to prepare the board session
    max_retries = 3
    for attempt in range(max_retries):
        try:
            board.prepare_session()
            print("Session prepared successfully.")
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} - Error preparing session: {e}")
            time.sleep(5)  # Wait before retrying
    else:
        print("Failed to prepare session after multiple attempts.")
        return

    # Start streaming
    try:
        board.start_stream()
        print("Streaming started.")
    except Exception as e:
        print(f"Error starting stream: {e}")
        return

    # Allow some time for data to accumulate
    time.sleep(10)

    # Stop streaming and release the board
    try:
        board.stop_stream()
        print("Streaming stopped.")
        data = board.get_board_data()
        print("Data retrieved.")
    except Exception as e:
        print(f"Error stopping stream: {e}")
        return

    board.release_session()
    print("Session released.")

    # Process the data
    eeg_channels = BoardShim.get_eeg_channels(board_id)
    eeg_data = data[eeg_channels, :]

    # Apply filters (e.g., bandpass filter)
    for channel in eeg_channels:
        DataFilter.perform_bandpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 1.0, 50.0, 4, FilterTypes.BUTTERWORTH.value, 0.5)
        DataFilter.perform_bandstop(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 48.0, 52.0, 4, FilterTypes.BUTTERWORTH.value, 0.5)
        DataFilter.perform_detrend(eeg_data[channel], DetrendOperations.LINEAR.value)

    # Basic analysis - calculating mean and variance
    for i, channel in enumerate(eeg_channels):
        print(f"Channel {channel}: Mean = {np.mean(eeg_data[i])}, Variance = {np.var(eeg_data[i])}")

if __name__ == "__main__":
    main()
