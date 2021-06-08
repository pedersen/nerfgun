#include <Arduino.h>

#include "bt.h"

const int loopdelay = 8 ;  // number of milliseconds for main loop to run, used to calculate how long to sleep when
                           // exiting main loop
unsigned long previousMillis = 0;  // will store last time loop was run, start with 0 for when the system starts up

const int baudrate = 9600;  // Serial interface for debugging, baudrate

void setup() {
    // establish display is available
    //  configure display
    // establish keyboard matrixes are available
    //  configure keyboard matrixes
    // establish imu is available
    //  wait until device is calibrated
    //  configure imu
    // establish bluetooth device is available
    //  configure bluetooth
    Serial.begin(baudrate);
    bt::setup();
    Serial.println("Ready with super setup!");
}

void loop() {
    unsigned long currentmillis = millis();
    if (currentmillis - previousMillis < loopdelay) {
        return; // not enough time has passed, and we are limiting ourselves to run once every loopdelay ms
    }
/*
    if (bluetooth.availableForWrite() == 0) {
        return;
    }
*/
    // read key status and send key events
    // read imu and send mouse motion events / mouse click events
    // update display as needed
    while (bt::available()) {
        Serial.print(bt::read());
    }
    while (Serial.available()) {
        bt::print(Serial.read());
    }
    if (digitalRead(bt::baud_rate_pin) == HIGH) {
        bt::switch_baud_rate();
    }
    if (digitalRead(bt::config_pin) == HIGH) {
        bt::reset();
    }
}
