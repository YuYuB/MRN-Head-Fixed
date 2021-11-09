int S;
int E;
int X;


int StartingVariable = 0;

void setup() {
  // put your setup code here, to run once:
pinMode(9,OUTPUT);
pinMode(8, INPUT);
pinMode(LED_BUILTIN, OUTPUT);
Serial.begin(115200);
}

void loop() {
S = digitalRead(8);
  // put your main code here, to run repeatedly:
//analogWrite(9,80);

if (S & !E & StartingVariable == 0) {
  Serial.print("START");
StartingVariable = StartingVariable + 1;
}
/*
if (StartingVariable == 1 & X < 2401){  
analogWrite(9,100); //50/80 gives about 5mW/10mW (473nm Laser)
delay(10);
analogWrite(9,0); //50 gives about 5mW (473nm Laser)
delay(40);
X = X+1;
Serial.println(X);
if(X == 1201){delay(60000);}
}

*/

if (S) {
analogWrite(9,250); //50/80 gives about 5mW/10mW (473nm Laser); 250 is the max (~20mW)
delay(10);
analogWrite(9,0); //0 stops the laser (473nm Laser)
delay(40);
  
}

else {analogWrite(9,0);}

}
