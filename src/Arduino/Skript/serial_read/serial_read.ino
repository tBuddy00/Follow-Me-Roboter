#include <Adafruit_MotorShield.h>
#include <Wire.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"


Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motorr = AFMS.getMotor(2);
Adafruit_DCMotor *Motorl = AFMS.getMotor(3);

const int bufferSize = 50; // Adjust the buffer size according to your needs
char inputBuffer[bufferSize]; // Array to store received characters
int numbersArray[bufferSize]; // Array to store parsed numbers
int index = 0; // Index to keep track of the current position in the arrays

int desired_speed_right = 0;
int desired_speed_left = 0;

int time0 = 0;

void setup() {
  Serial.begin(9600); // Set the baud rate to 9600

  AFMS.begin();
  Motorr->setSpeed(0);
  Motorl->setSpeed(0);
  
  // Initialize the buffers with null characters
  for (int i = 0; i < bufferSize; i++) {
    inputBuffer[i] = '\0';
    numbersArray[i] = 0;
  }
}

void loop() {
  
  if (Serial.available() > 0) { // Check if data is available to read
    char receivedChar = Serial.read(); // Read the incoming byte
    
    // Check if the received character is a newline or carriage return
    if (receivedChar == '\n' || receivedChar == '\r') {
      // End of line detected, process the received string
      processString();
    } else {
      // Store the received character in the buffer
      inputBuffer[index] = receivedChar;
      index++;
      
      // Check if the buffer is full
      if (index >= bufferSize - 1) {
        // Buffer overflow, process the received string
        processString();
      }
    }
  }
}

void processString() {
  // Print the received string
  Serial.print("Received: ");
  Serial.println(inputBuffer);

  // Parse the received string into numbers
  char *token = strtok(inputBuffer, ","); // Split the string by space
  int i = 0;
  while (token != NULL && i < bufferSize) {
    numbersArray[i] = atoi(token); // Convert the token to an integer
    token = strtok(NULL, ",");
    i++;
  }

  set_speed();
  
  // Reset the index and clear the buffers
  index = 0;
  for (int j = 0; j < bufferSize; j++) {
    inputBuffer[j] = '\0';
    numbersArray[j] = 0;
  }
  
}

void set_speed () {
  
  int speed_right = numbersArray[0];
  int speed_left = numbersArray[1];
  int speed_time = numbersArray[2];

  Serial.print("Speed Right: ");
  Serial.println(speed_right);
  Serial.print("Speed Left: ");
  Serial.println(speed_left);
  Serial.print("Speed Duration: ");
  Serial.println(speed_time);

  // set right motor
  if (speed_right > 0) { 
    Serial.println("Right FORWARD");
    desired_speed_right = speed_right;
    Motorr->run(FORWARD); 
  }
  else if (speed_right < 0){
    Serial.println("Right BACKWARD");
    Serial.println(speed_right * -1);
    desired_speed_right = speed_right * -1;
    Motorr->run(BACKWARD);
  }
  else {
    Serial.println("Right RELEASE");
    Motorr->run(RELEASE);
  }

  // set left motor
  if (speed_left > 0) {
    Serial.println("Left FORWARD");
    desired_speed_left = speed_left;
    Motorl->run(FORWARD);    
  }
  else if (speed_left < 0){
    Serial.println("Left BACKWARD");    
    Serial.println(speed_left * -1);
    desired_speed_left = speed_left * -1;
    Motorl->run(BACKWARD); 
  }
  else {
    Serial.println("Left RELEASE");
    Motorl->run(RELEASE);
  }

  time0 = millis();
  gradual_speed_increase();

  delay(speed_time);
  set_speed_0();
  
}

void gradual_speed_increase() {
  int num_steps = 5; // Number of steps for gradual increase
  int time_duration = 500; // in ms
  int step_duration = time_duration / num_steps;
  int speed_increment_right = desired_speed_right / num_steps;
  int speed_increment_left = desired_speed_left / num_steps;

  int current_speed_right = 0;
  int current_speed_left = 0;

  for (int i = 0; i < num_steps; i++) {
    current_speed_right += speed_increment_right;
    current_speed_left += speed_increment_left;
    Motorr->setSpeed(current_speed_right);
    Motorl->setSpeed(current_speed_left);
    delay(step_duration);
  }

  // Ensure the final desired speed is set
  Motorr->setSpeed(desired_speed_right);
  Motorl->setSpeed(desired_speed_left);
}

void set_speed_0 () {
  Serial.println("All motors RELEASE");
  int time1 = millis();
  int time2 = time1 - time0;
  Serial.println("Runtime: ");
  Serial.println(time2);
  Motorr->run(RELEASE);
  Motorl->run(RELEASE);
  Motorr->setSpeed(0);
  Motorl->setSpeed(0);
}