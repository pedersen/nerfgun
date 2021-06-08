#include "bt.h"
#include <SoftwareSerial.h>

namespace bt {
    // TX-O pin of bluetooth mate, Arduino D2
    const int bluetoothTx = 10;
    // RX-I pin of bluetooth mate, Arduino D3
    const int bluetoothRx = 11;
    SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

    const int cmd_delay = 500; // how much to delay after starting command mode
    const int init_baudrate = 115200;  // bluetooth speed during initialization, bluesmirf starts at this speed
    const int running_baudrate = 19200;  // bluetooth speed after initialization
    const String running_baudrate_str = "19.2"; // bluetooth baud rate as string for the bt modem
    const String device_name = "Nerf AR-L Controller";

    void setup() {
        switch_baud_rate();
        Serial.println("done configuring bluetooth module!");
    }

    void start_command_mode(int multiplier = 1) {
        Serial.println("$$$ ::: Entering command mode");
        bluetooth.print("$$$");
        delay(cmd_delay * multiplier);
    }

    void end_command_mode() {
        bluetooth.println("---");
    }

    void send_command(String command, String message, int multiplier=1) {
        Serial.println(command + " ::: " + message);
        bluetooth.println(command);
        delay(cmd_delay * multiplier);
    }

    void reset() {
        Serial.println("Applying config");
        start_command_mode();
        send_command("SF,1", "Factory reset");
        send_command("R,1", "Reboot", 5);

        switch_baud_rate();
        start_command_mode();
        send_command("SM,6", "Switch to Pairing Mode (vs Slave, Master, DTR)");
        send_command("SO,%", "Print out CONNECT/DISCONNECT messages for debugging");
        send_command("SH,0033", "Set HID flags to be keyboard/combo mouse");
        send_command("S~,6", "Switch to HID mode");
        send_command("SN," + device_name, "Set device name");
        send_command("SQ,16", "Switch to low latency mode");
        send_command("R,1", "Reboot", 5);
        Serial.println("Settings applied, bluetooth rebooted");
    }

    void switch_baud_rate() {
        bluetooth.begin(init_baudrate);
        start_command_mode();
        send_command("U," + running_baudrate_str + ",N", "Changing baudrate to " + running_baudrate_str);
        //send_command("R,1", "Reboot for baud rate change", 5);
        bluetooth.begin(running_baudrate);
    }

    int available() {
        return bluetooth.available();
    }

    int read() {
        return bluetooth.read();
    }

    size_t print(int ch) {
        return bluetooth.print(ch);
    }

    size_t print(String str) {
        return bluetooth.print(str.c_str());
    }

    size_t println(String str) {
        return bluetooth.print(str.c_str()) +
            bluetooth.println("");
    }
}
