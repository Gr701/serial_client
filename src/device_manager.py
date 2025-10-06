import json
import time
import serial.tools.list_ports
import colorama

colorama.init()

def load_allowed_devices():
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
    #return '/app/ttyV1'
    dot_count = 1
    while True:
        time.sleep(0.2)
        print('Looking for connected devices' + ('.' * dot_count))
        print('\033[F\033[K', end='')
        dot_count = (dot_count + 1) % 4
        for candidate in allowed_devices:
            for port in serial.tools.list_ports.comports():
                if port.vid is not None and port.pid is not None:
                    #print(f"port.vid={port.vid} port.pid={port.pid}")
                    if port.vid == candidate['vendorId'] and port.pid == candidate['productId']:
                        print('Found device: ', candidate['name'])
                        return port.device
