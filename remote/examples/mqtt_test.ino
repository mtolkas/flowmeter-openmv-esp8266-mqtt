#include <ESP8266WiFi.h>
#include <PubSubClient.h>
 
const char* ssid = "XXXX";
const char* password =  "XXXX";
const char* mqttServer = "XXXX";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
 
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, 1883);
//  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client")) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
//  client.publish("omv", "Hello from ESP8266"); 
}
 
void loop() {
  client.loop();
  client.publish("omv", "Hello World!"); 
  delay(2000);
}