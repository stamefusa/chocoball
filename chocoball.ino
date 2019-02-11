#include <Servo.h>

Servo servo1, servo2;
int num1 = 0, num2 = 0;
String str = "";
int state = -1, pre_state = -1;
unsigned long start_time = 0;

void setup(){
  servo1.attach(7);
  servo2.attach(8);
  num1 = 90;
  motor1(num1);
  num2 = 90;
  motor2(num2);
  Serial.begin(9600);

  start_time = millis();
}

void loop(){
  
  if(Serial.available() > 0){
    //データの読み込み
    state = int(Serial.read()) - 48;
    Serial.println(state);
    
    if (state == 0) {
      num1 = 90;
      num2 = 90;
    } else if (state == 1) {
      num1 = 5;
      num2 = 90;
    } else if (state == 2) {
      num1 = 175;
      num2 = 120;
    } else if (state == 3) {
      num1 = 175;
      num2 = 30;
    }
    motor1(num1);
    motor2(num2);

    start_time = millis();

    pre_state = state;
  }

  if (millis() - start_time > 2000) {
    num1 = 90;
    num2 = 90;
    pre_state = -1;
    motor1(num1);
    motor2(num2);
  }
  
  delay(100);
}

void motor1(int num) {
  servo1.write(num);
}

void motor2(int num) {
  servo2.write(num);
}
