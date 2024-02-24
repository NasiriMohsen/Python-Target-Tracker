#include <Servo.h>
#include <BluetoothSerial.h>

BluetoothSerial Bluetooth;

Servo XServo;
Servo YServo;

String StringData;

void setup() {
  XServo.attach(32);
  YServo.attach(33);

  XServo.write(90);
  YServo.write(90);
  
  Serial.begin(115200);
  Bluetooth.begin("Tracker");
}

void loop() {
  while (Bluetooth.available()) {
    char Data = Bluetooth.read();
    StringData += Data;
  }
  if (StringData.length() > 0) {
    int XValue = StringData.substring(0, StringData.indexOf(',')).toInt();
    XServo.write(XValue);
    
    int YValue = StringData.substring(StringData.indexOf(',') + 1).toInt();
    YServo.write(YValue);

    Serial.print("X Value: ");
    Serial.print(XValue);
    Serial.print(" ,Y Value: ");
    Serial.println(YValue);
    StringData = "";
  }
}
