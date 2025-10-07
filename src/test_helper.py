"""Module to help in testing the main program. Reads the input, adds \r\n and sends to main program. To open the serial between the main program and this program socat can be used:
    socat PTY,link=/app/ttyV0,raw,echo=0 PTY,link=/app/ttyV1,raw,echo=0"""
import serial
uart = serial.Serial('ttyV0', 9600, timeout=0)
while True:
    us = input()
    uart.write(f"{us}".replace('\\0', '\0').encode('utf-8'))
    incoming = uart.read(100).decode('utf-8', errors='ignore')
    print(incoming.encode())

