#include <XL320.h>
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <HttpClient.h>

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
  server.on("/actuate", xl_wheel);
  server.on("/detach", xl_detach);
  server.on("/detect", detect_rfid);
  server.begin();

 
}

void loop() {
  server.handleClient();
}

void xl_wheel() {
  String data = server.arg("plain");
  StaticJsonDocument<200> jObject;
  deserializeJson(jObject, data);
  String id = jObject["id"];
  String velocity = jObject["speed"];
  
  XLservo.setJointSpeed(id.toInt(), velocity.toInt());
  server.send(204, "");
}

void xl_detach() {
//  XLservo.setJointSpeed(6, 800);
  XLservo.moveJoint(6, 800);
  delay(2000);
  XLservo.moveJoint(6, 200);
  server.send(204, "");
}

void detect_rfid() {

  StaticJsonDocument<200> data;
  data["object"] = "can opener";

  String data_string;
  serializeJson(data, data_string);
  
  server.sendContent(data_string);
}
