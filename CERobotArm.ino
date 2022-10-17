
#include <Stepper.h>

const int stepsPerRevolution = 2000;  // change this to fit the number of steps per revolution
const int steps1PerRevolution = 2000;
const int basediv = 142;
const int rot1div = 944;//?
const int rot2div = 144;
const int scale= 10;

const int J1stepPin = 8;
const int J1dirPin = 9;
const int J2stepPin = 6;
const int J2dirPin = 7;
const int J3stepPin = 10;
const int J3dirPin = 11;

#define PI 3.1415926535897932384626433832795

float thet0=0;
float thet1=0;
float thet2=PI/2;

int delayvar = 10;

int16_t buf[300];
int16_t Ary[50];
int16_t thd0[50];
int16_t thd1[50];
int16_t thd2[50];
String inData ;
String th0;
String th1;
String th2;
uint16_t i=0, j=0;



Stepper baseStepper(stepsPerRevolution, 8, 9); // step 8 dir 9 
Stepper rot1Stepper(steps1PerRevolution, 6, 7);
Stepper rot2Stepper(stepsPerRevolution, 10, 11);



void stepper2(int J1step, int J2step, int J3step){
  int curDelay = 20;
  int J1cur = 0;
  int J2cur = 0;
  int J3cur = 0;
  int J1el;
  int J2el;
  int J3el;
  int J1stepabs;
  int J2stepabs;
  int J3stepabs;

  J1stepabs=abs(J1step);
  J2stepabs=abs(J2step);
  J3stepabs=abs(J3step);


   if (J1step < 0)
  {
    J1el=-1;
  }
  else if (J1step > 0)
  {
    J1el=1;
  }


  if (J2step < 0)
  {
    J2el=-1;
  }
  else if (J2step > 0)
  {
    J2el=1;
  }


  if (J3step < 0)
  {
    J3el=-1;
  }
  else if (J3step > 0)
  {
    J3el=1;
  }

  ///// DRIVE MOTORS /////
  while (J1cur < J1stepabs || J2cur < J2stepabs || J3cur < J3stepabs)
  {
    int csicska = 10;

    while (csicska > 0){
      /////// J2 ////////////////////////////////
      if (J2cur < J2stepabs)
      {
        J2cur = ++J2cur;
        rot1Stepper.step(J2el);
        delayMicroseconds(curDelay);
      }
      csicska--;
    } 
    /////// J3 ////////////////////////////////
    if (J3cur < J3stepabs)
    {
      J3cur = ++J3cur;
      rot2Stepper.step(J3el);
      delayMicroseconds(curDelay);
    }

    if (J1cur < J1stepabs)
    {
      J1cur = ++J1cur;
      baseStepper.step(J1el);
      delayMicroseconds(curDelay);
    }
  }
}


void odavisz(){
  for (int i=0; i<sizeof thd0/sizeof thd0[0]; i++) {
    stepper2(thd0[i], thd1[i], thd2[i]);
    //delay(5);
  }
}


void manual(){

  char inChar = Serial.read();
  long int inInt = Serial.parseInt();
  Serial.println(inChar);
  Serial.println(inInt);

  //1.tengely
  if (inChar=='q') {
    // 85000 lépés 90 fok 30000 lépés 3.5 mp ami 32 fok    250 speed
    baseStepper.step(inInt);

    thet0=thet0+inInt/basediv;
    Serial.println(thet0);
  }
  // 12800 lépés 90 fok 100 speed 1 fok 142 lépés
  if (inChar=='e') {
    baseStepper.step(-inInt);
    thet0=thet0-inInt/basediv;
    Serial.println(thet0);
  }

  //1.tengely
  if (inChar=='d') {
    // 85000 lépés 90 fok 30000 lépés 3.5 mp ami 32 fok    250 speed
    rot1Stepper.step(inInt);

    thet1=thet1+inInt/rot1div;
    Serial.println(thet1);
  }
  
  if (inChar=='a') {
    rot1Stepper.step(-inInt);
    thet1=thet1-inInt/rot1div;
    Serial.println(thet1);
  }

  //2. tengely
  if (inChar=='l') {
    rot2Stepper.step(inInt);
    thet2=thet2+inInt/rot2div;
    Serial.println(thet2);
  }
  
  if (inChar=='j') {
    rot2Stepper.step(-inInt);
    thet2=thet2-inInt/rot2div;
    Serial.println(thet2);
    //15,4 másodperc 1 félkör 180 fok és 26000 lépés 50-es speedel

    //kiegészíteni szögszámolással
    //mozgási idők meghatározása ha a szög megvan
  }
}


void printintdb(int16_t* buf, int len){
  for (int i = 0; i < len; i++) {
    Serial.println(buf[i]);
  }
}


void stringIntArray(String msg2,int16_t* Ary){
  uint8_t i=0, j=0;
  int sz;
  char carray[7];
  for (int j = 0; j<msg2.length(); j++)  {
    
    if (msg2.charAt(j)==','){
      int n;
      n = atoi(carray); 
      Ary[i]=n;
      i++;
      sz=0;
      carray[7]=' ';
      carray[6]=' ';
      carray[5]=' ';
      carray[4]=' ';
      carray[3]=' ';
      carray[2]=' ';
      carray[1]=' ';
      carray[0]=' ';
    }
    else{
      carray[sz]=msg2.charAt(j);
      sz++;
    }
  }
}


void setup() {

  Serial.begin(9600);
  baseStepper.setSpeed(100);
  rot1Stepper.setSpeed(250);
  rot2Stepper.setSpeed(50);

}

void loop() {

  if (Serial.available() > 0) {
    inData = Serial.readString();
  
  

    int th0end=inData.indexOf('B');
    int th1end=inData.indexOf('N');
    int th2end=inData.indexOf('M');

    String th0 = inData.substring(0,th0end-1);
    String th1 = inData.substring(th0end+1,th1end);
    String th2 = inData.substring(th1end+1,th2end);
    
    Serial.println(th2);
    stringIntArray(th0,thd0);
    stringIntArray(th1,thd1);
    stringIntArray(th2,thd2);

    printintdb(thd2,10);


    odavisz();
  }
}
