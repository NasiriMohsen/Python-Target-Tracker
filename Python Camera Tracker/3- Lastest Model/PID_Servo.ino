#include <Servo.h>

Servo XServo;
Servo YServo;

int XAngle,YAngle;

String Input,XInput,YInput;

char InputChar;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  
  XServo.attach(5);
  YServo.attach(6);
}

void loop() {
  Input = "";
  if (Serial.available()){
    while (Serial.available()){
      InputChar = Serial.read();
      //Serial.println(InputChar);

      if (InputChar == ','){
        XInput = Input;
        Input = "";
      }
      else if (InputChar == '.'){
        YInput = Input;
        Input = "";
      }
      else{
        Input = Input + InputChar;
        //Serial.println(Input);
      }
    }
    XAngle = XInput.toInt();
    YAngle = YInput.toInt();
    
    XServo.write(XAngle);
    YServo.write(YAngle);
    
    Serial.print("XServo,YServo: ");
    Serial.print(XAngle);
    Serial.print(",");
    Serial.println(YAngle);
  }
delay(100);
}
