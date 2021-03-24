
// Wifi Libraries/Variables
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Arduino_JSON.h>

const char* ssid = "esp8266_test";    // Replace with name of your wifi network
const char* password = "mmmmmmmmmm";  // Replace with password of your wifi network

String cardData;

String motion_string[2];  //Dummy payload. Gets the upper and lower limit of motion from the server
String motion_double[2];  //Dummy payload converted to doubles

// Node-RED server address (Could work with a different type of server as long as the code is the same, but I have not tested it)
const char* serverWrite = "http://192.168.97.62:1880/write_card";
const char* serverRead = "http://192.168.97.62:1880/read_data";



// RFID Libraries/Variables
#include <SoftwareSerial.h>
SoftwareSerial rSerial(4, 5); // RX, TX
const int tagLen = 16;
const int idLen = 13;

char newTag[idLen];
char tagID[idLen] = "000000000000";



// Program setup
void setup() {
  // Serial Monitor
  Serial.begin(115200);
  
  // RFID Reader
  rSerial.begin(9600);

  // Wifi initialization
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Ready to read card!");
}



// Program loop
void loop() {
  // Read the card's ID
  bool check = false;
  while (check == false)
    check = tagNumber(tagID);
  Serial.write(tagID, idLen);
  Serial.println();
  
  //Check WiFi connection status, then upload the card's ID to the server
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    
    // Your Domain name with URL path or IP address with path
    http.begin(serverWrite);

    http.addHeader("Content-Type", "application/json");
    
    String payload = "{\"ID\":\"";
    payload.concat(tagID);
    payload.concat("\"}");

    Serial.println(payload);
    
    int httpResponseCode = http.POST(payload);
   
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }

  // Wait 5 seconds for the server to finish processing (if necessary)
  delay(5000);

  // Check Wifi connection status, then read 
  if(WiFi.status()== WL_CONNECTED){
          
    cardData = httpGETRequest(serverRead);
    Serial.println(cardData);
    JSONVar myObject = JSON.parse(cardData);
    
    // JSON.typeof(jsonVar) can be used to get the type of the var
    if (JSON.typeof(myObject) == "undefined") {
      Serial.println("Parsing input failed!");
      return;
    }
    
    Serial.print("JSON object = ");
    Serial.println(myObject);
    
    // myObject.keys() can be used to get an array of all the keys in the object
    JSONVar keys = myObject.keys();
    
    for (int i = 2; i < keys.length(); i++) {
      JSONVar value = myObject[keys[i]];
      Serial.print(keys[i]);
      Serial.print(" = ");
      Serial.println(value);
      motion_string[i - 2] = value;                           // Need this step because JSONVar doesn't contain a function to convert to double
      motion_double[i - 2] = motion_string[i - 2].toDouble();
    }
  }

  // Here you can have code that uses the motion values on the ESP! (Or any other values that you decide to include in the JSON)
  Serial.println(motion_double[0]);
  Serial.println(motion_double[1]);
  
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