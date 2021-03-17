/*
  Control of x4 whole body motion. 4 servos.
  Upper two: Micro servo 9g
  Lower two: Dynamixel XL 320
  4 motions: turn; bow; nod; shake.
*/

#include <XL320.h>
//#include <Servo.h>
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
//#include <HalfDuplexHardwareSerial.h>

XL320 XLservo;
SoftwareSerial XLSerial(D7, D8); // (RX pin 3, TX pin 1)

void setup(){
  XLSerial.begin(115200);
//  Serial.println();
//  Serial.print("ESP8266 Board MAC Address:  ");
//  Serial.println(WiFi.macAddress());

//  XLSerial.begin(XLSerial);
  XLservo.begin(XLSerial);
  
  delay(1000);
}
 
void loop(){
//  Serial.println();
//  Serial.print("ESP8266 Board MAC Address:  ");
//  Serial.println(WiFi.macAddress());
//  delay(1000);
//  XLservo.TorqueON(7);
  XLservo.setJointSpeed(7, 2047);

  delay(150);
  XLservo.setJointSpeed(7, 1023);

  delay(150);
//  XLservo.setJointSpeed(7, 300);
//
//  delay(1000);

}
