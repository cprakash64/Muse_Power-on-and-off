from pythonosc import dispatcher
from pythonosc import osc_server
import serial
import time

# Set up the serial connection to Arduino
arduino = serial.Serial('/dev/tty.usbmodem14201', 9600)  # Update with your Arduino port

def send_command_to_arduino(command):
    arduino.write(command.encode())

# Example threshold values, adjust as necessary
threshold_off = 50
threshold_blink = 100

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    print(f"EEG (uV) per channel: {ch1}, {ch2}, {ch3}, {ch4}")
    # Process EEG data to determine command
    avg_eeg = (ch1 + ch2 + ch3 + ch4) / 4
    if avg_eeg < threshold_off:
        send_command_to_arduino('0')  # Turn off light
        time.sleep(1)  # Wait for 1 second
        send_command_to_arduino('1')  # Turn on light
    elif avg_eeg < threshold_blink:
        send_command_to_arduino('2')  # Blink light

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/muse/eeg", eeg_handler, "EEG")

ip = "192.168.116.215"
port = 5000  # Ensure this matches the port set in Muse Lab

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
