#include "keyboard.h"

const int baudrate=9600;

void setup() {
  Serial.begin(baudrate);
  // establish display is available
  //  configure display
  // establish keyboard matrixes are available
  //  configure keyboard matrixes
  // establish imu is available
  //  wait until device is calibrated
  //  configure imu
  // establish bluetooth device is available
  //  configure bluetooth
  Serial.println("Ready!");
}

void loop() {
  // if bluetooth is available *and* connected
  //    read key configuration and send key events
  //    read imu and send mouse motion events
  //    update display as needed
}
