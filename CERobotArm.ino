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

#define PI 3.1415926535897932384626433832795

float thet0=0;
float thet1=0;
float thet2=PI/2;

int delayvar = 10;


int16_t thd0[50];
int16_t thd1[50];
int16_t thd2[50];


Stepper baseStepper(stepsPerRevolution, 8, 5); // step 8 dir 9
Stepper rot1Stepper(steps1PerRevolution, 6, 7);
Stepper rot2Stepper(stepsPerRevolution, 10, 11);


void calculator(int32_t J1step, int32_t J2step, int32_t J3step)
{
  int curDelay = 1;
  int J1cur = 0;
  int J2cur = 0;
  int J3cur = 0;
  int J1el;
  int J2el;
  int J3el;
  int a;
  int b;
  int c;

  a=abs(J1step);
  b=abs(J2step);
  c=abs(J3step);


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

  const int32_t max_step_size = 1;
  int32_t biggest = a;
  if (b > biggest)
    biggest = b;
  if (c > biggest)
    biggest = c;

  int32_t number_of_steps = ceil(biggest/max_step_size);

  double avg_a = (double)a / (double)number_of_steps;
  double avg_b = (double)b / (double)number_of_steps;
  double avg_c = (double)c / (double)number_of_steps;

  int32_t a_done = 0;
  int32_t b_done = 0;
  int32_t c_done = 0;

  for (int i = 0; i < number_of_steps; ++i) {
    int32_t curr_a = floor(avg_a*i);
    curr_a -= a_done;
    int32_t curr_b = floor(avg_b*i);
    curr_b -= b_done;
    int32_t curr_c = floor(avg_c*i);
    curr_c -= c_done;

    a -= curr_a;
    b -= curr_b;
    c -= curr_c;

    a_done += curr_a;
    b_done += curr_b;
    c_done += curr_c;

    baseStepper.step(curr_a*J1el);
    delayMicroseconds(curDelay);
    rot1Stepper.step(curr_b*J2el);
    delayMicroseconds(curDelay);
    rot2Stepper.step(curr_c*J3el);
    delayMicroseconds(curDelay);

  }
};

void odavisz(){
  for (int i=0; i<sizeof thd0/sizeof thd0[0]; i++) {
    calculator(thd0[i], thd1[i], thd2[i]);
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

}


uint8_t bytes[320];
int indexBuff=0;


void loop() {


  while (Serial.available() > 0) {

    //manual();


    Serial.setTimeout(10);
    int len = Serial.readBytes(bytes,320);

    //uint8_t bytes[] = {56,130,87,0,85,0,83,0,81,0,79,0,78,0,76,0,74,0,73,0,71,0,70,0,68,0,67,0,65,0,64,0,63,0,61,0,60,0,59,0};

    switch (indexBuff) {
      case 0:
        //Serial.println("th0");
        for (int i=0; i<len;i=i+2){
          int16_t result_0 = read_int16_t(bytes, i);
          //Serial.println(result_0);
          thd0[i/2]=result_0;
        }
        break;
      case 1:
        //Serial.println("th0");
        for (int i=0; i<len;i=i+2){
          int16_t result_0 = read_int16_t(bytes, i);
          //Serial.println(result_0);
          thd0[i/2]=result_0;
        }
        break;

      case 2:
        //Serial.println("th1");
        for (int i=0; i<len;i=i+2){
          int16_t result_0 = read_int16_t(bytes, i);
          //Serial.println(result_0);
          thd1[i/2]=result_0;
        }
        break;

      case 3:
        //Serial.println("th2");
        for (int i=0; i<len;i=i+2){
          int16_t result_0 = read_int16_t(bytes, i);
          //Serial.println(result_0);
          thd2[i/2]=result_0;
        }
        break;
      default:

          indexBuff=0;
        break;

    }

    if (indexBuff==3){
      odavisz();
    }
    indexBuff++;
  }
}
