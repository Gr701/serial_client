import os
import time
import serial
import threading
import queue
import colorama

import morse
import device_manager

colorama.init()

user_input = queue.Queue()
def get_user_input():
    while not restart_event.is_set():
        print('>', end='')
        inp = input()
        if inp == '.exit':
            exit_event.set()
            restart_event.set()
        elif inp == '.clear':
            print('\033[2J\033[H', end='')
            continue
        user_input.put(inp)
        print('\033[F\033[K', end='')

def send_data(uart):
    while not restart_event.is_set():
        time.sleep(1)
        if not user_input.empty():
            morse_string = morse.encode(user_input.get())
            for c in morse_string:
                if c == ' ':
                    time.sleep(1)
                    continue
                uart.write(f"{c}\r\n".encode('utf-8'))
                time.sleep(0.5)

def get_data(uart):
    incoming_message = ''
    while not restart_event.is_set():
        time.sleep(0.1)
        try:
            incoming_char = uart.read(50).decode('utf-8', errors='ignore')
            if incoming_char:
                incoming_char = incoming_char.strip('\r\n\0')
                print('\r\033[K' + incoming_char + '\n>', end='')
                incoming_message += incoming_char
                if '   ' in incoming_message:
                    print('\r' + morse.decode(incoming_message) + '\n>', end='')
                    incoming_message = ''
        except serial.SerialException:
            restart_event.set()

allowed_devices = None
restart_event = threading.Event()
exit_event = threading.Event()
def main():
    global allowed_devices
    print('Loading config file')
    allowed_devices = device_manager.load_allowed_devices()
    if allowed_devices is None:
        print('Invalid config.json file')
        return
    print('Config loaded with ', len(allowed_devices), ' devices')

    while not exit_event.is_set():
        device = device_manager.find_connected_device(allowed_devices)
        uart = serial.Serial(device, 9600, timeout=0)
        print('Connected\n')

        input_thread = threading.Thread(target=get_user_input)
        send_data_thread = threading.Thread(target=send_data, args=(uart,))
        get_data_thread = threading.Thread(target=get_data, args=(uart,))

        input_thread.start()
        send_data_thread.start()
        get_data_thread.start()

        input_thread.join()
        send_data_thread.join()
        get_data_thread.join()

        restart_event.clear()

main()
