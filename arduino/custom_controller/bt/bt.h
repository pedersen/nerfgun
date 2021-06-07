//
// Created by marvin on 6/3/21.
//

#ifndef CUSTOM_CONTROLLER_BT_H
#define CUSTOM_CONTROLLER_BT_H

#include <Arduino.h>
#include <SoftwareSerial.h>

namespace bt {
    // bluetooth adapter/handler
    extern SoftwareSerial bluetooth;
    const int baud_rate_pin = 2;
    const int config_pin = 4;

    extern void setup();
    extern void reset();
    extern void switch_baud_rate();
    extern void start_command_mode();
}

#endif //CUSTOM_CONTROLLER_BT_H
