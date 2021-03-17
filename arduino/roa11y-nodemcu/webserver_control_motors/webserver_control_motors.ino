#include <XL320.h>
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

const char* ssid     = "MieMie";
const char* password = "lijiahao";

ESP8266WebServer server;

XL320 XLservo;
SoftwareSerial XLSerial(D7, D8); // (RX pin 3, TX pin 1)

void setup() {
  Serial.begin(9600);

  
  XLSerial.begin(115200);
  XLservo.begin(XLSerial);

  delay(1000);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/",[](){server.send(200,"text/plain","Hellow World!");});
  server.on("/test", test_dynamixel);
  server.begin();

 
}

void loop() {
  server.handleClient();
}

void test_dynamixel() {
  String data = server.arg("plain");
  StaticJsonBuffer<200> jBuffer;
  JsonObject& jObject = jBuffer.parseObject(data);
  String id = jObject["id"];
  String velocity = jObject["speed"];
  
  XLservo.setJointSpeed(id.toInt(), velocity.toInt());
  server.send(204, "");
}
