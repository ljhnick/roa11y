/*
  Control of x4 whole body motion. 4 servos.
  Upper two: Micro servo 9g
  Lower two: Dynamixel XL 320
  4 motions: turn; bow; nod; shake.
*/

#include <XL320.h>
#include <Servo.h>
#include <SoftwareSerial.h>

XL320 XLservo;
SoftwareSerial XLSerial(10, 11); // (RX pin 10, TX pin 11)
static int turnID = 13;
static int bowID = 12;
Servo nod;
Servo shake;

static int pi = 3.14159;

/*
 * neutural position of servos
 */
float tturn = 0;
float tbow = 24;
float tnod = 0;
float tshake = 75;
float lasttnod = 0;
float lasttshake = 0;
float deltatnod = 0;
float deltatshake = 0;
int motorspeed = 100;

int defaultmotorspeed = 100; //default Dynamixel motor speed
int actionms = 1000; // milliseconds to finish action
int repeat = 1; //numbers of repeat for some actions
int afterms = 1000; //milliseconds after action
int delaytime = 0;

int n = 0;

class Action {
  public:

  //=============== SLEEP ===============
  //Parameter: actionms; afterms;
  void Sleep() {
    lasttnod = tnod;
    lasttshake = tshake;
    tturn = 0;
    tbow = 24;
    tnod = 0;
    tshake = 75;

    motorspeed = 100000/actionms;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = actionms/100;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }

    delay(afterms);
  }


  //=============== NEUTRAL POSITION ===============
  //Parameter: actionms; afterms;
  void Neutral() {
    lasttnod = tnod;
    lasttshake = tshake;
    tturn = 0;
    tbow = 0;
    tnod = 30;
    tshake = 75;

    motorspeed = 100000/actionms;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = actionms/100;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }

    delay(afterms);
  }


  //=============== LEAN FORWARD ===============
  //Parameter: actionms; afterms;
  void LeanForward() {
    lasttnod = tnod;
    lasttshake = tshake;
    tturn = 0;
    tbow = 24;
    tnod = 80;
    tshake = 75;

    motorspeed = 100000/actionms;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = actionms/100;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }

    delay(afterms);
  }


  //=============== NOD ===============
  //Parameter: repeat; afterms;
  void Nod() {
    /* starting position
    tturn = 0;
    tbow = 0;
    tnod = 30;
    tshake = 75;
    */
    
    //raising head phase
    tturn = 0;
    tbow = -5;
    tnod = 50;
    tshake = 75;
    motorspeed = 400;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    nod.write(tnod);
    shake.write(tshake);
    delay(200);

    //nodding phase
    int nrepeat = 100*repeat;
    for (n = 0; n<nrepeat; n+=1) {
      tturn = 0;
      tbow = 5 - abs(10*cos(0.01*n*pi));
      tnod = 0 + abs(50*cos(0.01*n*pi));
      tshake = 75;
      XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
      XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
      nod.write(tnod);
      shake.write(tshake);
      //delay(1); 
    }

    //returning to neutral position phase
    tturn = 0;
    tbow = 0;
    tnod = 30;
    tshake = 75;
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    nod.write(tnod);
    shake.write(tshake);
    
    delay(afterms);
  }


  //=============== LOOK TO THE RIGHT ===============
  //Parameter: actionms; afterms;
  void LookRight() {
    lasttnod = tnod;
    lasttshake = tshake;
    
    tturn = 40;
    tbow = 20;
    tnod = 80;
    tshake = 75-50;
    
    motorspeed = 100000/actionms;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = actionms/100;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }
    
    delay(afterms);
  }


  //=============== ALL JOINTS ROTATION ===============
  //Parameter: repeat; afterms;
  void Rotate() {
    tturn = 40;
    tbow = 0;
    tnod = 30;
    tshake = 75+70;
    XLservo.setJointSpeed(turnID, defaultmotorspeed); delay(2);
    XLservo.setJointSpeed(bowID, defaultmotorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    nod.write(tnod);
    shake.write(tshake);
    delay(200);

    motorspeed = 400;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    int nrepeat = 100*repeat;
    for (n = 0; n<nrepeat; n+=1) {
      tturn = 40*cos(0.01*2*n*pi);
      tbow = 3 + 12*sin(0.01*2*n*pi);
      tnod = 30 + 30*sin(0.01*2*n*pi);
      tshake = 75 + 70*cos(0.01*2*n*pi);
      XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
      XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
      nod.write(tnod);
      shake.write(tshake);
      delay(8); // use delay to control micro servo speed
    }
    tturn = 0;
    tbow = 0;
    tnod = 30;
    tshake = 75;
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    nod.write(tnod);
    shake.write(tshake);
    
    delay(afterms);
  }

  //=============== SCAN RIGHT TO LEFT ===============
  //Parameter: repeat; afterms;
  void Scan() {
    lasttnod = tnod;
    lasttshake = tshake;
    tturn = 0 + 40;
    tbow = 24;
    tnod = 5 + 7;
    tshake = 75 - 25;

    //looking down phase
    motorspeed = 100;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = 10;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }
    delay(1000);

    //scaning phase
    motorspeed = 400;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    int nrepeat = 100*repeat;
    for (n = 0; n<nrepeat; n+=1) {
      tturn = 40*cos(0.01*2*n*pi);
      tbow = 24;
      tnod = 5+abs(7*cos(0.01*2*n*pi));
      tshake = 75-25*cos(0.01*2*n*pi);
      XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
      XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
      nod.write(tnod);
      shake.write(tshake);
      delay(25); 
    }
    delay(1000);

    //returning to neutral position phase
    lasttnod = tnod;
    lasttshake = tshake;
    tturn = 0;
    tbow = 0;
    tnod = 30;
    tshake = 75;

    motorspeed = 100;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = 12;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }

    delay(afterms);
  }

  //=============== LOOK AROUND RIGHT TO LEFT ===============
  //Parameter: repeat; afterms;
  void LookAround() {
    lasttnod = tnod;
    lasttshake = tshake;
    tturn = 0 + 50;
    tbow = 0 + 15;
    tnod = 30 + 30;
    tshake = 75 - 50;

    //look right phase
    motorspeed = 100;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = 10;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }
    delay(500);

    //scaning phase
    motorspeed = 400;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    int nrepeat = 100*repeat;
    for (n = 0; n<nrepeat; n+=1) {
      tturn = 50*cos(0.01*2*n*pi);
      tbow = abs(15*cos(0.01*2*n*pi));
      tnod = 30+abs(30*cos(0.01*2*n*pi));
      tshake = 75-50*cos(0.01*2*n*pi);
      XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
      XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
      nod.write(tnod);
      shake.write(tshake);
      delay(20); 
    }
    delay(300);

    //returning to neutral position phase
    lasttnod = tnod;
    lasttshake = tshake;
    tturn = 0;
    tbow = 0;
    tnod = 30;
    tshake = 75;

    motorspeed = 150;
    XLservo.setJointSpeed(turnID, motorspeed); delay(2);
    XLservo.setJointSpeed(bowID, motorspeed); delay(2);
    XLservo.moveJoint(turnID, (tturn*13/8+150)*1023/300); delay(2);
    XLservo.moveJoint(bowID, (2*tbow+150)*1023/300); delay(2);
    
    deltatnod = (tnod - lasttnod)/100;
    deltatshake = (tshake - lasttshake)/100;
    delaytime = 12;
    for (n=0; n<100; n+=1) {
      tnod = lasttnod + deltatnod*n;
      tshake = lasttshake + deltatshake*n;
      nod.write(tnod);
      shake.write(tshake);
      delay(delaytime);
    }

    delay(afterms);
  }
};

  /*
   * lower neck motion XL servo
   * bit = (1023/300)*(angle+150)
   * angle range -150 ~ 150 deg
   * 
   * tturn
   * neutural position of turning: 0
   * smallest: -92.3 deg (left); largest: 92.3 deg (right)
   * considering 8:13 reduction ratio
   * 
   * tbow
   * neutural position of bowing: 0
   * smallest: -17 deg; largest: 24 deg (bow)
   * 
   * based on real bowing angle, not servo actuation angle
   * considering 1:2 reduction ratio
   * 
   * speed unit: 0.666 deg/second
   */

  /*
   * upper neck motion micro servo
   * 
   * tnod
   * neutural position of nodding: 30 deg
   * smallest: 0 deg (nod); largest: 80 deg
   * 
   * tshake
   * neutural position of shaking: 75 deg
   * smallest: 0 deg (right); largest: 180 deg (left)
   */


Action act;

void setup() {
  XLSerial.begin(115200);
  XLservo.begin(XLSerial);
  XLservo.setJointSpeed(turnID, defaultmotorspeed); delay(5);// turn speed 0~1023
  XLservo.setJointSpeed(bowID, defaultmotorspeed); delay(5);// bow speed 0~1023

  
  nod.attach(8); // nod pin 8
  shake.attach(9); //shake pin 9
  delay(100);
}

void loop() {
  /* Action List:
  
  actionms = 1000; afterms = 3500; act.Sleep();
  actionms = 1000; afterms = 2500; act.Neutral();
  actionms = 1000; afterms = 2500; act.LeanForward();
  repeat = 5;      afterms = 1000; act.Nod();
  actionms = 1000; afterms = 2500; act.LookRight();
  repeat = 5;      afterms = 1000; act.Rotate();
  repeat = 5;      afterms = 2000; act.Scan();
  repeat = 2;      afterms = 2000; act.LookAround();
  
  */

  actionms = 1000; afterms = 3500; act.Sleep();
  actionms = 1000; afterms = 2500; act.Neutral();
  repeat = 1;      afterms = 300; act.LookAround();
  actionms = 1000; afterms = 3000; act.LeanForward();
  actionms = 1000; afterms = 300; act.Neutral();
  repeat = 3;      afterms = 2000; act.Nod();
  
  repeat = 5;      afterms = 1000; act.Rotate();
}
