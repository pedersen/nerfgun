//
// Created by marvin on 6/3/21.
//

#include "bt/bt.h"

namespace bt {
    // TX-O pin of bluetooth mate, Arduino D2
    const int bluetoothTx = 10;
    // RX-I pin of bluetooth mate, Arduino D3
    const int bluetoothRx = 11;

    SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

    const int init_baudrate = 115200;  // bluetooth speed during initialization, bluesmirf starts at this speed
    const int running_baudrate = 19200;  // bluetooth speed after initialization
    const char* running_baudrate_str = "19.2"; // bluetooth baud rate as string for the bt modem
    const char* device_name = "Nerf AR-L Controller";
    const int cmd_delay = 500; // how much to delay after starting command mode
    void setup() {
        switch_baud_rate();
        bluetooth.begin(running_baudrate);
        bluetooth.println("C");
        Serial.println("done config!");
    }

    void start_command_mode() {
        bluetooth.print("$");  // Print three times individually
        bluetooth.print("$");
        bluetooth.print("$");  // Enter command mode
    }

    void end_command_mode() {
        bluetooth.println("---");
    }

    void reset() {
        Serial.println("Applying config");
        start_command_mode();
        bluetooth.println("SF,1"); // factory reset
        bluetooth.println("R,1"); // reboot
        Serial.println("Factory reset, rebooting");
        delay(cmd_delay*5);

        start_command_mode();
        bluetooth.println("SM,4"); // use DTR mode to automatically store last BT ID that connected
        delay(cmd_delay);
        bluetooth.println("SO,%"); // print out CONNECT/DISCONNECT messages for debugging
        delay(cmd_delay);
        bluetooth.println("S~,6"); // Switch to HID mode
        delay(cmd_delay);  // Short delay, wait for the Mate to send back CMD
        Serial.println("switched to HID mode");
        bluetooth.println("SH,0033"); // HID keyboard, combo mouse, joystick
        delay(cmd_delay);  // Short delay, wait for the Mate to send back CMD
        Serial.println("Switch to kbd/mouse");
        bluetooth.print("SN,");
        bluetooth.println(device_name); // set device name
        Serial.println("Switched device name");
        delay(cmd_delay);  // Short delay, wait for the Mate to send back CMD
        bluetooth.println("SQ,16");  // low latency mode (instead of high throughput mode)
        delay(cmd_delay);  // Short delay, wait for the Mate to send back CMD
        Serial.println("Switched to low latency");
        delay(cmd_delay);  // Short delay, wait for the Mate to send back CMD
        bluetooth.println("R,1");
        delay(cmd_delay*10);
        Serial.println("Settings applied, bluetooth rebooted");
    }

    void switch_baud_rate() {
        bluetooth.begin(init_baudrate);  // The Bluetooth Mate defaults to 115200bps
        start_command_mode();
        delay(cmd_delay);  // Short delay, wait for the Mate to send back CMD
        bluetooth.print("U,");
        bluetooth.print(running_baudrate_str);
        bluetooth.println(",N");  // Temporarily Change the baudrate to running baud rate, no parity
        // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
        bluetooth.begin(running_baudrate);  // Start bluetooth serial at running_baud_rate
        delay(cmd_delay);
    }

}

