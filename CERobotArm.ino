#include <Stepper.h>
#include <assert.h>

const int stepsPerRevolution = 2000;  // change this to fit the number of steps per revolution
const int steps1PerRevolution = 2000;
const int basediv = 142;
const int rot1div = 944;//?
const int rot2div = 144;
const int scale= 10;

const int J1stepPin = 8;
const int J1dirPin = 5;
const int J2stepPin = 6;
const int J2dirPin = 7;
const int J3stepPin = 10;
const int J3dirPin = 11;
const int J4stepPin = 23;
const int J4dirPin = 25;
const int J5stepPin = 12;
const int J5dirPin = 13;
const int J6stepPin = 9;
const int J6dirPin = 4;

#define PI 3.1415926535897932384626433832795

float thet0=0;
float thet1=0;
float thet2=PI/2;

int delayvar = 10;


int16_t thd0[50];
int16_t thd1[50];
int16_t thd2[50];
int16_t thd3[50];
int16_t thd4[50];
int16_t thd5[50];

Stepper baseStepper(stepsPerRevolution, J1stepPin, J1dirPin); // step 8 dir 9
Stepper rot1Stepper(steps1PerRevolution, J2stepPin, J2dirPin);
Stepper rot2Stepper(stepsPerRevolution, J3stepPin, J3dirPin);
Stepper J4Stepper(stepsPerRevolution, J4stepPin, J4dirPin);
Stepper J5Stepper(stepsPerRevolution, J5stepPin, J5dirPin);
Stepper J6Stepper(stepsPerRevolution, J6stepPin, J6dirPin);

void calculator(int16_t J1step, int16_t J2step, int16_t J3step, int16_t J4step, int16_t J5step, int16_t J6step)
{
  int curDelay = 1;
  int J1cur = 0;
  int J2cur = 0;
  int J3cur = 0;
  int J4cur = 0;
  int J5cur = 0;
  int J6cur = 0;

  int J1el;
  int J2el;
  int J3el;
  int J4el;
  int J5el;
  int J6el;

  int J1abs;
  int J2abs;
  int J3abs;
  int J4abs;
  int J5abs;
  int J6abs;

  J1abs=abs(J1step);
  J2abs=abs(J2step);
  J3abs=abs(J3step);
  J4abs=abs(J4step);
  J5abs=abs(J5step);
  J6abs=abs(J6step);


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


  if (J4step < 0)
  {
    J4el=-1;

  }
  else if (J4step > 0)
  {
    J4el=1;
  }


  if (J5step < 0)
  {
    J5el=-1;
  }
  else if (J5step > 0)
  {
    J5el=1;
  }


  if (J6step < 0)
  {
    J6el=-1;
  }
  else if (J6step > 0)
  {
    J6el=1;
  }

  const int32_t max_step_size = 1;
  int32_t biggest = J1abs;
  if (J2abs > biggest)
    biggest = J2abs;
  if (J3abs > biggest)
    biggest = J3abs;
  if (J4abs > biggest)
    biggest = J4abs;
  if (J5abs > biggest)
    biggest = J5abs;
  if (J6abs > biggest)
    biggest = J6abs;

  int32_t number_of_steps = ceil(biggest/max_step_size);

  double avg_J1 = (double)J1abs / (double)number_of_steps;
  double avg_J2 = (double)J2abs / (double)number_of_steps;
  double avg_J3 = (double)J3abs / (double)number_of_steps;
  double avg_J4 = (double)J4abs / (double)number_of_steps;
  double avg_J5 = (double)J5abs / (double)number_of_steps;
  double avg_J6 = (double)J6abs / (double)number_of_steps;

  int32_t J1_done = 0;
  int32_t J2_done = 0;
  int32_t J3_done = 0;
  int32_t J4_done = 0;
  int32_t J5_done = 0;
  int32_t J6_done = 0;

  for (int i = 0; i < number_of_steps; ++i) {
    int32_t curr_J1 = floor(avg_J1*i);
    curr_J1 -= J1_done;
    int32_t curr_J2 = floor(avg_J2*i);
    curr_J2 -= J2_done;
    int32_t curr_J3 = floor(avg_J3*i);
    curr_J3 -= J3_done;
    int32_t curr_J4 = floor(avg_J4*i);
    curr_J4 -= J4_done;
    int32_t curr_J5 = floor(avg_J5*i);
    curr_J5 -= J5_done;
    int32_t curr_J6 = floor(avg_J6*i);
    curr_J6 -= J6_done;

    J1abs -= curr_J1;
    J2abs -= curr_J2;
    J3abs -= curr_J3;
    J4abs -= curr_J4;
    J5abs -= curr_J5;
    J6abs -= curr_J6;

    J1_done += curr_J1;
    J2_done += curr_J2;
    J3_done += curr_J3;
    J4_done += curr_J4;
    J5_done += curr_J5;
    J6_done += curr_J6;

    baseStepper.step(curr_J1*J1el);
    delayMicroseconds(curDelay);
    rot1Stepper.step(curr_J2*J2el);
    delayMicroseconds(curDelay);
    rot2Stepper.step(curr_J3*J3el);
    delayMicroseconds(curDelay);
    J4Stepper.step(curr_J4*J4el);
    delayMicroseconds(curDelay);
    J5Stepper.step(curr_J5*J5el);
    delayMicroseconds(curDelay);
    J6Stepper.step(curr_J6*J6el);
    delayMicroseconds(curDelay);

  }
};

void odavisz(){
  for (int i=0; i<sizeof thd0/sizeof thd0[0]; i++) {
    calculator(thd0[i], thd1[i], thd2[i], thd3[i], thd4[i], thd5[i]);
    //Serial.println(thd0[i]);
    //Serial.println(thd1[i]);
    //Serial.println(thd2[i]);
    delay(5);
  }
  Serial.println("k");
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



int16_t read_int16_t(uint8_t* ByteArray, size_t offset)
{
  return *((int16_t *)&ByteArray[offset]);
}

void setup() {

  Serial.begin(115200);
  baseStepper.setSpeed(100);
  rot1Stepper.setSpeed(250);
  rot2Stepper.setSpeed(50);
  J4Stepper.setSpeed(50);
  J5Stepper.setSpeed(50);
  J6Stepper.setSpeed(50);
}


uint8_t bytes[520];
int indexBuff=0;
int arrayzero[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int arraypos[20] ={100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100};
int arrayneg[20] = {-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100};

void loop() {

  while (Serial.available() > 0) {

    //manual();


    Serial.setTimeout(10);
    int len = Serial.readBytes(bytes,520);

    //int len[] = {56,130,87,0,85,0,83,0,81,0,79,0,78,0,76,0,74,0,73,0,71,0,70,0,68,0,67,0,65,0,64,0,63,0,61,0,60,0,59,0};


    switch (indexBuff) {
      case 0:

        for (int i=0; i<len;i=i+2){
          int16_t result_0 = read_int16_t(bytes, i);
          //Serial.println(result_0);
          thd0[i/2]=result_0;
        }
        break;

      case 1:

        for (int i=0; i<len;i=i+2){
          int16_t result_0 = read_int16_t(bytes, i);
          //Serial.println(result_0);
          thd0[i/2]=result_0;
        }
        //Serial.println("th0");
        break;

      case 2:

        for (int i=0; i<len;i=i+2){
          int16_t result_1 = read_int16_t(bytes, i);
          //Serial.println(result_1);
          thd1[i/2]=result_1;
        }
        //Serial.println("th1");
        break;

      case 3:

        for (int i=0; i<len;i=i+2){
          int16_t result_2 = read_int16_t(bytes, i);
          //Serial.println(result_2);
          thd2[i/2]=result_2;
        }
        //Serial.println("th2");
        break;

      case 4:
        //Serial.println("th3");
        for (int i=0; i<len;i=i+2){
          int16_t result_3 = read_int16_t(bytes, i);
          //Serial.println(result_3);
          thd3[i/2]=result_3;
        }
        break;

      case 5:
        //Serial.println("th4");
        for (int i=0; i<len;i=i+2){
          int16_t result_4 = read_int16_t(bytes, i);
          //Serial.println(result_4);
          thd4[i/2]=result_4;
        }
        break;

      case 6:
        //Serial.println("th5");
        for (int i=0; i<len;i=i+2){
          int16_t result_5 = read_int16_t(bytes, i);
          //Serial.println(result_5);
          thd5[i/2]=result_5;
        }
        break;


      default:

          indexBuff=0;
        break;

    }

    if (indexBuff==6){
      odavisz();
    }
    indexBuff++;
  }


}
