# Remote Control - As The Remote Device
#
# This script configures your OpenMV Cam as a co-processor that can be remotely controlled by
# another microcontroller or computer such as an Arduino, ESP8266/ESP32, RaspberryPi, and
# even another OpenMV Cam.
#
# This script is designed to pair with "popular_features_as_the_controller_device.py".

import image, network, math, rpc, sensor, struct, tf

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

# The RPC library above is installed on your OpenMV Cam and provides mutliple classes for
# allowing your OpenMV Cam to be controlled over CAN, I2C, SPI, UART, USB VCP, or WiFi.

################################################################
# Choose the interface you wish to control your OpenMV Cam over.
################################################################


# Uncomment the below line to setup your OpenMV Cam for control over SPI.
#
# * cs_pin - Slave Select Pin.
# * clk_polarity - Idle clock level (0 or 1).
# * clk_phase - Sample data on the first (0) or second edge (1) of the clock.
#
# NOTE: Master and slave settings much match. Connect CS, SCLK, MOSI, MISO to CS, SCLK, MOSI, MISO.
#       Finally, both devices must share a common ground.
#
# interface = rpc.rpc_spi_slave(cs_pin="P3", clk_polarity=1, clk_phase=0)

# Uncomment the below line to setup your OpenMV Cam for control over UART.
#
# * baudrate - Serial Baudrate.
#
# NOTE: Master and slave baud rates must match. Connect master tx to slave rx and master rx to
#       slave tx. Finally, both devices must share a common ground.
#
interface = rpc.rpc_uart_slave(baudrate=115200)

################################################################
# Call Backs
################################################################

# Helper methods used by the call backs below.

def draw_detections(img, dects):
    for d in dects:
        c = d.corners()
        l = len(c)
        for i in range(l): img.draw_line(c[(i+0)%l] + c[(i+1)%l], color = (0, 255, 0))
        img.draw_rectangle(d.rect(), color = (255, 0, 0))

# Remote control works via call back methods that the controller
# device calls via the rpc module on this device. Call backs
# are functions which take a bytes() object as their argument
# and return a bytes() object as their result. The rpc module
# takes care of moving the bytes() objects across the link.
# bytes() may be the micropython int max in size.


# When called returns the payload string for the largest qrcode
# within the OpenMV Cam's field-of-view.
#
# data is unused
def qrcode_detection(data):
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.VGA)
    codes = sensor.snapshot().find_qrcodes()
    if not codes: return bytes() # No detections.
    draw_detections(sensor.get_fb(), codes)
    return max(codes, key = lambda c: c.w() * c.h()).payload().encode()

# When called returns a json list of json qrcode objects for all qrcodes in view.
#
# data is unused
def all_qrcode_detection(data):
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.VGA)
    sensor.set_windowing((320, 240))
    codes = sensor.snapshot().find_qrcodes()
    if not codes: return bytes() # No detections.
    draw_detections(sensor.get_fb(), codes)
    return str(codes).encode()

# Register call backs.

interface.register_callback(qrcode_detection)
# interface.register_callback(all_qrcode_detection)

# Once all call backs have been registered we can start
# processing remote events. interface.loop() does not return.

interface.loop()
