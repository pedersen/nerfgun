//
// Created by marvin on 6/3/21.
//

#ifndef CUSTOM_CONTROLLER_BT_H
#define CUSTOM_CONTROLLER_BT_H

#include <Arduino.h>

namespace bt {
    // bluetooth adapter/handler
    const int baud_rate_pin = 2;
    const int config_pin = 4;

    extern void setup();
    extern void reset();
    extern void switch_baud_rate();
    extern void start_command_mode(int multiplier);
    extern int available();
    extern int read();
    extern size_t print(int ch);
    extern size_t print(String str);
    extern size_t println(String str);
}

#endif //CUSTOM_CONTROLLER_BT_H
