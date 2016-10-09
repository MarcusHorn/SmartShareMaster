/*
 * Arduino code by Marcus Horn for
 */

#include <CurieBLE.h>
#include <Servo.h>

Servo myservo; // Initializes servo

BLEPeripheral board; // Initializes Bluetooth on the board
BLEService servoControl("2ca7b03e-8309-47e3-bf97-517a57dfaffb"); // Randomized UUID 

// BLE Servo Mode - Modified through Bluetooth
BLEUnsignedCharCharacteristic servoToggle("2ca7b03f-8309-47e3-bf97-517a57dfaffb", BLERead | BLEWrite);

int pos = 0; // Position of servo
int maxR = 180;
int minR = 0;
int rotRate = 1; // Parameters for motion of servo
int jiggleThresh = 120; // Position to fluctuate from during demo

int travelDelay = 15; // Delay of 15 ms during rotation
int motionDelay = 2000; // 2 secs delay between parts of demo

void setup() {
  Serial.begin(9600);
  
  myservo.attach(9); // Sets servo to pin 9

  myservo.write(pos); // Sets servo to zero position at start

  // Local name and service UUID
  board.setLocalName("SmrtShre");
  board.setAdvertisedServiceUuid(servoControl.uuid());

  // Attribute and characteristics
  board.addAttribute(servoControl);
  board.addAttribute(servoToggle);

  // Initial value for characteristic
  servoToggle.setValue(0);

  board.begin();

  Serial.println("Servo Controller"); 
}

void loop() {
    BLECentral central = board.central();

    if (central) {
      Serial.print("Connected to central: ");
      Serial.println(central.address());

      while (central.connected()) {
        if (servoToggle.written()) {
          if (servoToggle.value()) {
            Serial.println("Servo ON");
            rotateServo();
            servoToggle.setValue(0);
            Serial.println("Servo OFF");
          }
        }
      }
    }
    else if (Serial.available() > 0) {
      while (Serial.available() > 0) {
        char curChar = (char)Serial.read();
        if (curChar == '\n') {
          continue;
        }
      }
      Serial.println(Serial.read(), DEC);
      Serial.println("Servo ON");
      rotateServo();
      servoToggle.setValue(0);
      Serial.println("Servo OFF");
    }
}

void rotateServo() {
  for(pos = minR; pos <= maxR; pos += rotRate) { // Forward rotation
    myservo.write(pos);
    delay(travelDelay);
  }
  delay(motionDelay);
  for(pos = maxR; pos >= jiggleThresh; pos -= rotRate) { // Partial backwards rotation
    myservo.write(pos);
    delay(travelDelay);
  }
  for(pos = jiggleThresh; pos <= maxR; pos += rotRate) { // Partial forwards rotation
    myservo.write(pos);
    delay(travelDelay);
  }
  delay(motionDelay);
  for(pos = maxR; pos >= minR; pos -= rotRate) { // Full backwards rotation
    myservo.write(pos);
    delay(travelDelay);
  }
}

