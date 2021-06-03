#include <Arduino.h>
#include <SoftwareSerial.h>
#include "keyboard.h"

const int baudrate=9600;

const int bluetoothTx = 2;  // TX-O pin of bluetooth mate, Arduino D2
const int bluetoothRx = 3;  // RX-I pin of bluetooth mate, Arduino D3

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

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
    Serial.println("hello world");
    delay(2500);
}
