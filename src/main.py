"""2-way communication client for the final project of Computer Systems-course in University of Oulu using UART and Morse code."""
import os
import time
import serial
import threading
import queue
import colorama

import morse
import device_manager

colorama.init() #allows the use of ANSI escape codes in cmd on Windows (\033[K, \033[F)

user_input = queue.Queue()
def get_user_input():
    """Get the input from the console and add it to the user_input queue. Special commands are .clear and .exit"""
    while not restart_event.is_set():
        print('>', end='')
        inp = input()
        if inp == '.exit':
            exit_event.set() #signal to main to exit
            restart_event.set() #signal to threads to stop
        elif inp == '.clear':
            print('\033[2J\033[H', end='') #clear the terminal and move cursor to upper left corner
            continue
        user_input.put(inp)
        print('\033[F\033[K', end='') #clear line to hide the user input after pressing enter

def send_data(uart):
    """Get data from the user_input queue. Encode the data to morse and send by one character over uart."""
    while not restart_event.is_set():
        time.sleep(1)
        if not user_input.empty():
            morse_string = morse.encode(user_input.get())
            for c in morse_string:
                if c == ' ': #don't send spaces
                    time.sleep(1)
                    continue
                uart.write(f"{c}\r\n".encode('utf-8'))
                time.sleep(0.5)

def get_data(uart):
    """Get the data from uart. Print to the console. If 3 spaces are met decode the message and print it to console."""
    incoming_message = ''
    while not restart_event.is_set():
        time.sleep(0.1)
        try:
            incoming_char = uart.read(50).decode('utf-8', errors='ignore')
            if incoming_char:
                incoming_char = incoming_char.strip('\r\n\0')
                print('\r\033[K' + incoming_char + '\n>', end='') #clear current line before printing
                incoming_message += incoming_char
                if '   ' in incoming_message: #3 spaces
                    print('\r' + morse.decode(incoming_message) + '\n>', end='')
                    incoming_message = ''
        except serial.SerialException:
            restart_event.set() #if device is disconnected signal threads to stop 

allowed_devices = None
restart_event = threading.Event()
exit_event = threading.Event()
def main():
    """Load the config. Enter main loop, where the connected device is found and communication threads are started. If device is disconnected the restart_event is set. Threads are stopped and the next loop iteration begins with looking for connected device."""
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

        get_data_thread.join()
        input_thread.join(timeout=1)
        send_data_thread.join(timeout=1)

        restart_event.clear()

main()
