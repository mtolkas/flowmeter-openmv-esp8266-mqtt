#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <openmvrpc.h>


// WiFi and communication config
const char *ssid = "<SSID>";
const char *password = "<PASSWORD>";
const char *mqtt_server = "192.168.1.15";
const char *mqtt_topic = "omv";

WiFiClient espClient;
PubSubClient client(espClient);

//  OpenMV config
openmv::rpc_scratch_buffer<256> scratch_buffer; 
openmv::rpc_hardware_serial_uart_master interface(115200);

void setup_wifi()
{
    delay(10);

    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void reconnect()
{
    // Loop until we're reconnected
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        // Create a random client ID
        String clientId = "ESP8266Client-";
        clientId += String(random(0xffff), HEX);
        // Attempt to connect
        if (client.connect(clientId.c_str()))
        {
            Serial.println("connected");
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void setup()
{
    // OpenMV 
    interface.begin();

    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
}

// OpenMV Call Back Handler
char* exec_flow_meter_read()
{
    char buff[128 + 1] = {}; // null terminator
    // The function name below must match the callback name in the OMV remote script
    if (interface.call_no_args(F("flow_meter_read"), buff, sizeof(buff) - 1)) {
        // Serial.println("buff");
        // Serial.println(buff);
        return buff;
    }
}

void loop()
{
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();

    // Execute remote function on OMV
    char* result = exec_flow_meter_read();
    Serial.print("Latest reading: ");
    Serial.print(result);

    // Send to MQTT broker
    client.publish(mqtt_topic, result);
    // delay(1000);
}