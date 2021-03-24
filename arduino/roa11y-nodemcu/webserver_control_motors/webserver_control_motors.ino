#include <XL320.h>
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
//#include <HttpClient.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Arduino_JSON.h>
//
//const char* ssid = "esp8266_test";    // Replace with name of your wifi network
//const char* password = "mmmmmmmmmm";  // Replace with password of your wifi network

const char* ssid     = "MieMie";
const char* password = "lijiahao";


// RFID part initialization
String cardData;

String motion_string[2];  //Dummy payload. Gets the upper and lower limit of motion from the server
String motion_double[2];  //Dummy payload converted to doubles

// Node-RED server address (Could work with a different type of server as long as the code is the same, but I have not tested it)
//const char* serverWrite = "http://192.168.97.62:1880/write_card";
//const char* serverRead = "http://192.168.97.62:1880/read_data";

// comment the below when necessary
const char* serverWrite = "http://192.168.86.246:1880/write_card";
const char* serverRead = "http://192.168.86.246/read_data";
const char* serverActuate = "http://192.168.86.246:1880/actuate";
const char* serverDetach = "http://192.168.86.246/detach";

SoftwareSerial rSerial(4, 5); // RX, TX
const int tagLen = 16;
const int idLen = 13;

char newTag[idLen];
char tagID[idLen] = "";

String dataSend = "";


// motor part initialization
ESP8266WebServer server;

XL320 XLservo;
SoftwareSerial XLSerial(D7, D8); // (RX pin 3, TX pin 1)

void setup() {
  Serial.begin(57600);

  // RFID serial
  rSerial.begin(9600);

  // Motor serial
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

  
  // Read the card's ID
  bool check = false;
//  while (check == false)
  check = tagNumber(tagID);
//  Serial.write(tagID, idLen);
//  Serial.println();
//    Serial.println(tagID);
  dataSend = "{\"ID\":\"";
  dataSend.concat(tagID);
  dataSend.concat("\"}");
    
  
  //Check WiFi connection status, then upload the card's ID to the server
//  if(WiFi.status()== WL_CONNECTED){
//    HTTPClient http;
//    
//    // Your Domain name with URL path or IP address with path
//    http.begin(serverWrite);
//
//    http.addHeader("Content-Type", "application/json");
//    
//    String payload = "{\"ID\":\"";
//    payload.concat(tagID);
//    payload.concat("\"}");
////
////    Serial.println(payload);
//    
//    int httpResponseCode = http.POST(payload);
////   
////    Serial.print("HTTP Response code: ");
////    Serial.println(httpResponseCode);
//    
//    http.end();
//  }
//  else {
//    Serial.println("WiFi Disconnected");
//  }
//
//  // Wait 5 seconds for the server to finish processing (if necessary)
////  delay(5000);
//
//  // Check Wifi connection status, then read 
//  if(WiFi.status()== WL_CONNECTED){
//          
//    cardData = httpGETRequest(serverRead);
//    Serial.println(cardData);
//    JSONVar myObject = JSON.parse(cardData);
//    
//    // JSON.typeof(jsonVar) can be used to get the type of the var
//    if (JSON.typeof(myObject) == "undefined") {
//      Serial.println("Parsing input failed!");
//      return;
//    }
//    
//    Serial.print("JSON object = ");
//    Serial.println(myObject);
//    
//    // myObject.keys() can be used to get an array of all the keys in the object
//    JSONVar keys = myObject.keys();
//    
//    for (int i = 2; i < keys.length(); i++) {
//      JSONVar value = myObject[keys[i]];
//      Serial.print(keys[i]);
//      Serial.print(" = ");
//      Serial.println(value);
//      motion_string[i - 2] = value;                           // Need this step because JSONVar doesn't contain a function to convert to double
//      motion_double[i - 2] = motion_string[i - 2].toDouble();
//    }
//  }
//
//  // Here you can have code that uses the motion values on the ESP! (Or any other values that you decide to include in the JSON)
//  Serial.println(motion_double[0]);
//  Serial.println(motion_double[1]);
  
}

void xl_wheel() {
  String data = server.arg("plain");
  StaticJsonDocument<200> jObject;
  deserializeJson(jObject, data);
  String id = jObject["id"];
  String velocity = jObject["speed"];

  server.send(204, "");
  XLservo.setJointSpeed(id.toInt(), velocity.toInt());
  
}

void xl_detach() {
//  XLservo.setJointSpeed(6, 800);
  XLservo.moveJoint(6, 800);
  delay(2000);
  XLservo.moveJoint(6, 200);
  server.send(204, "");
}

void detect_rfid() {

//  StaticJsonDocument<200> data;
//  data["object"] = "can opener";
//
//  String data_string;
//  serializeJson(data, data_string);
  Serial.print("1");
  
  server.sendContent(dataSend);
}

String httpGETRequest(const char* serverName) {
  HTTPClient http;
    
  // Your IP address with path or Domain name with URL path 
  http.begin(serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}

bool tagNumber(char* tagID){
  bool returnVal = false;
  
  int i = 0;
  int readByte;
  boolean tag = false;
  if (rSerial.available() == tagLen) {
    tag = true;
  }
  if (tag == true) {
    while (rSerial.available()) {
      // Take each byte out of the serial buffer, one at a time
      readByte = rSerial.read();
      if (readByte != 2 && readByte!= 13 && readByte != 10 && readByte != 3) {
        newTag[i] = readByte;
        i++;
      }
      // If we see ASCII 3, ETX, the tag is over
      if (readByte == 3) {
        tag = false;
      }
    }
  }
  if (strlen(newTag)== 0) {
    return false;
  }
  else {
    for (int i = 0; i < idLen; i++){
      tagID[i] = newTag[i];
    }
    returnVal = true;
  }
  for (int c=0; c < idLen; c++) {
    newTag[c] = 0;
  }
  return returnVal;
}
