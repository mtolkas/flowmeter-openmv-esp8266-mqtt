import time
from pyb import UART

# UART 3, and baudrate.
uart = UART(3, 115200)

while(True):
    uart.write("Hello World!\n")
    if (uart.any()):
        print(uart.read())
    time.sleep(1000)