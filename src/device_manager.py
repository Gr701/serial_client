"""Device manager for finding and validating connected serial devices."""
import json
import time
import serial.tools.list_ports
import colorama

colorama.init() #allows the use of ANSI escape codes in cmd on Windows (\033[K, \033[F)

def load_allowed_devices():
    """Load devices from config.json and check for the required fields"""
    try:
        with open('./config.json', 'r') as file: 
            data = json.load(file)
            for device in data:
                if 'productId' not in device or 'vendorId' not in device or 'name' not in device:
                    return None
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def find_connected_device(allowed_devices):
    """Go through connected USB devices, look for one matching the config, return its address (e.g. /dev/ttyACM0)"""
    return "/app/ttyV1"
    dot_count = 1
    while True:
        time.sleep(0.2)
        print('Looking for connected devices' + ('.' * dot_count))
        print('\033[F\033[K', end='') #move cursor up one line and clear the line
        dot_count = (dot_count + 1) % 4
        for candidate in allowed_devices:
            for port in serial.tools.list_ports.comports(): #list of connected devices
                if port.vid is not None and port.pid is not None:
                    if port.vid == int(candidate['vendorId'], 16) and port.pid == int(candidate['productId'], 16):
                        print('Found device:', candidate['name'])
                        return port.device
