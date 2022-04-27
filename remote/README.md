# Overview

This repo includes code to control an OpenMV (OMV) camera from a ESP8666 microcontroller using the [OpenMV Arudino RPC library](https://github.com/openmv/openmv-arduino-rpc).

The solution is comprised of two parts
 
 - Controller `arduino_controller.ino` sketch that needs to be uploaded to the esp8266 using Arduino IDE
 - The OpenMV micropython `main_openmv_remote.py` that needs to be added on the camera's filesystem (either internal or SD). Note that the file needs to be named `main.py` to run on boot. Here we are using a more descriptive filename for clarity.

 The ESP and OpenMV communicate using UART. The RPC libraries allows for additional protocolls but UART works well.

 # Arduino controller
 The controller runnng on the esp8266 is an MQTT client that subscribes to a particular topic of an MQTT broker and:
 * Runs a remote process on the camera - in this scope this is the meaurement of an analog flow meter.
 * Gets the result
 * Publishes the result to the MQTT broker

 # OpenMV 
* The OMV file includes the code for reading the reading of an analog flow meter and implented on this repo. 

**Note that the flow meter reading code has been adjusted to facilitate the remote control functionality. Therefore, if changes are made to the reading code, these should be adjusted here. This is needed until a proper coupling mechanism has been implemented**


# Connetion diagram
For both devices to communicate using UART, connect as follows.

* OMV Pin 4 (UART TX pin) <-> ESP RX pin
* OMV Pin 5 (UART RX pin) <-> ESP TX pin
* OMV GND <-> ESP GND


# Examples folder
In the exampes folder, there two simple applications to test the device communication without the length of the full fuel meter application. 

## Example 1: hello_world 
In this basic example, a bare minimum implemenetation of the UART protocol is provided, where OMV simply responds to the master ESP with a string. This can be used as a first step to ensure that ESP can read data from the OMV before more involved code is deployed.
* Deploy the `arduino_controller.ino` sketch to the ESP
* Add the content of `remote_openvmv.py` in a file named `main.py` in the root of the OMV's filesystem

After restarting both devices, the Serioal Monitor of the ESP should read the text "Hello World!" that is transmitted from the OMV.
After restarting both devices, the Serioal Monitor of the ESP should read the text "Hello World!" that is transmitted from the OMV.

## Example 2: qrcode
This application implements the OMV's QR code example - i.e. identifies the payload of QR code on the frame, and subsquently sends the result to the ESP.

For details about how this is achieved via callbacks, read the RPC library docs.