import serial
uart = serial.Serial('ttyV0', 9600, timeout=0)
while True:
    us = input()
    uart.write(f"{us}\r\n".encode('utf-8'))
