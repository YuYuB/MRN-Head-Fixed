 #include <Wire.h>
#include <Adafruit_MotorShield.h>
     
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 2);




int curPhotoState;                    // Current USPin State
int lstPhotoState;                    // Last USPin State

int RWD;
int X;
int EndX;
int Start = 0 ;
int Z = 0;

const int Photo = 7; 

unsigned long Delay;
unsigned long StartStamp;
unsigned long LightDelay;    

void setup() {
  
  pinMode(Photo, INPUT_PULLUP);
  pinMode(10, OUTPUT);
  pinMode(9, INPUT_PULLUP);
  pinMode(12, INPUT);
  Serial.begin(115200);
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  myMotor->setSpeed(80);  // 10 rpm  
}

void loop() {
/*if (digitalRead(12) == HIGH && Start == 0){
   myMotor->onestep(BACKWARD, DOUBLE);
   delay(1);
  }
  */
X = digitalRead(9);

curPhotoState   = digitalRead(Photo);  // Read Photo Pin

if (!X && EndX && Start == 0){
  Start = 1;
  Delay = millis();
  StartStamp = millis();
  Serial.print("5000");
  Serial.print(",");
  Serial.print(millis()-StartStamp);
  Serial.print(",");
  Serial.println();
  RWD=1;
}  


if (Start == 1) {
  if (!lstPhotoState && curPhotoState){
    Serial.print("8000");
    Serial.print(",");
    Serial.print(millis()-StartStamp);
    Serial.print(",");
    Serial.println();
  }

  if (millis() - Delay >= 10000){ 
    // 10000 for Laser at US onset; 8000 for Laser starts 2sec before US onset
   Z = 1; 
   LightDelay = millis();
  }

if (Z == 1){
  if (millis() - LightDelay <= 2000){
    digitalWrite(10, HIGH);
  }
  if (millis() - LightDelay > 2000){
    digitalWrite(10, LOW);
    Z = 0;
  }
}
 
  if (millis() - Delay >= 10000){
    RWD=1;
    //digitalWrite(10, LOW); // uncomment for 2s before US condition
    //Z = 0; // uncomment for 2s before US condition
    Serial.print("5000");
    Serial.print(",");
    Serial.print(millis()-StartStamp);
    Serial.print(",");
    Serial.println();
    Delay = millis();
  }


  if (RWD == 1){
    if (millis() - Delay <50){
    
    myMotor->onestep(FORWARD, DOUBLE);
    }
    else {RWD = 0;}
  }
  


 
 }


 lstPhotoState   = curPhotoState;
EndX = X;

delay(5);
}
