// Remote Control - As The Controller Device
//
// This script configures your Arduino to remotely control an OpenMV Cam using the RPC
// library.
//
// This script is designed to pair with "popular_features_as_the_remote_device.py" running
// on the OpenMV Cam. The script is in OpenMV IDE under Files -> Examples -> Remote Control. 

#include <openmvrpc.h>

// The RPC library above provides mutliple classes for controlling an OpenMV Cam over
// CAN, I2C, SPI, or Serial (UART).

// We need to define a scratch buffer for holding messages. The maximum amount of data
// you may pass in any on direction is limited to the size of this buffer.

openmv::rpc_scratch_buffer<256> scratch_buffer; // All RPC objects share this buffer.

// Uncomment the below line to setup your Arduino for controlling over SPI.
//
// * cs_pin - Slave Select Pin.
// * freq - SPI Bus Clock Frequency.
// * spi_mode - See (https://www.arduino.cc/en/reference/SPI)
//
// NOTE: Master and slave settings much match. Connect CS, SCLK, MOSI, MISO to CS, SCLK, MOSI, MISO.
//       Finally, both devices must share a common ground.
//
// openmv::rpc_spi_master interface(10, 1000000, SPI_MODE2);

// Uncomment the below line to setup your Arduino for controlling over a hardware UART.
//
// * baudrate - Serial Baudrate.
//
// NOTE: Master and slave baud rates must match. Connect master tx to slave rx and master rx to
//       slave tx. Finally, both devices must share a common ground.
//
// WARNING: The program and debug port for your Arduino may be "Serial". If so, you cannot use
//          "Serial" to connect to an OpenMV Cam without blocking your Arduino's ability to
//          be programmed and use print/println.
//
// openmv::rpc_hardware_serial_uart_master -> Serial
// openmv::rpc_hardware_serial1_uart_master -> Serial1
// openmv::rpc_hardware_serial2_uart_master -> Serial2
// openmv::rpc_hardware_serial3_uart_master -> Serial3
// openmv::rpc_hardware_serialUSB_uart_master
//
 openmv::rpc_hardware_serial_uart_master interface(115200);

void setup() {
    interface.begin();
    Serial.begin(115200);
}

//////////////////////////////////////////////////////////////
// Call Back Handlers
//////////////////////////////////////////////////////////////

void exe_qrcode_detection()
{
    char buff[128 + 1] = {}; // null terminator
    if (interface.call_no_args(F("qrcode_detection"), buff, sizeof(buff) - 1)) {
        Serial.println(buff);
    }
}
// Execute remote functions in a loop. Please choose and uncomment one remote function below.
// Executing multiple at a time may run slowly if the camera needs to change camera modes
// per execution.

void loop() {
     exe_qrcode_detection(); // Place the QRCode about 2ft away.
 