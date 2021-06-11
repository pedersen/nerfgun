/*
  Example Bluetooth Serial Passthrough Sketch
 by: Jim Lindblom
 SparkFun Electronics
 date: February 26, 2013
 license: Public domain

 This example sketch converts an RN-42 bluetooth module to
 communicate at 9600 bps (from 115200), and passes any serial
 data between Serial Monitor and bluetooth module.
 */
#include <SoftwareSerial.h>

const int serial_baud_rate = 9600 ;
const int bluetoothTx = 10;  // TX-O pin of bluetooth mate, Arduino D2
const int bluetoothRx = 11;  // RX-I pin of bluetooth mate, Arduino D3
const long int init_baudrate = 115200;  // bluetooth speed during initialization, bluesmirf starts at this speed
const int running_baudrate = 19200;  // bluetooth speed after initialization
const String running_baudrate_str = "19.2"; // bluetooth baud rate as string for the bt modem
const String device_name = "Nerf AR-L Controller";
const int cmd_delay = 500; // how much to delay after starting command mode (in ms)

const int baud_rate_pin = 2;
const int config_pin = 4;

const int loopdelay = 8;  // number of milliseconds for main loop to run, used to calculate how long to sleep when
                          // exiting main loop
unsigned long previousMillis = 0;  // will store last time loop was run, start with 0 for when the system starts up
SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void start_command_mode(int multiplier = 1) {
    Serial.println("$$$ ::: Entering command mode");
    bluetooth.print("$$$");
    delay(cmd_delay * multiplier);
}

void send_command(String command, String message, int multiplier=1) {
    Serial.println(command + " ::: " + message);
    bluetooth.println(command);
    delay(cmd_delay * multiplier);
}

void end_command_mode() {
    bluetooth.println("---");
}

void switch_baud_rate() {
    Serial.println("Switching baud rate");
    bluetooth.begin(init_baudrate);
    start_command_mode();
    send_command("U," + running_baudrate_str + ",N", "Changing baudrate to " + running_baudrate_str);
    bluetooth.begin(running_baudrate);
    delay(cmd_delay);
    end_command_mode();
}

void apply_config() {
    Serial.println("Applying bluetooth config");
    start_command_mode();
    send_command("SM,6", "Switch to Pairing Mode (vs Slave, Master, DTR)");
    send_command("SO,%", "Print out CONNECT/DISCONNECT messages for debugging");
    send_command("SH,0033", "Set HID flags to be keyboard/combo mouse");
    send_command("S~,6", "Switch to HID mode");
    send_command("SN," + device_name, "Set device name");
    send_command("SQ,16", "Switch to low latency mode");
    send_command("R,1", "Reboot", 5);
    switch_baud_rate();
    Serial.println("Settings applied, bluetooth rebooted");
}
void setup()
{
    Serial.begin(serial_baud_rate);  // Begin the serial monitor at 9600bps
    switch_baud_rate();
    pinMode(baud_rate_pin, INPUT);
    pinMode(config_pin, INPUT);
    Serial.println("setup complete!");
}

void loop() {
    unsigned long currentmillis = millis();
    if ((currentmillis - previousMillis) < loopdelay) {
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
    while(bluetooth.available() > 0)  // If the bluetooth sent any characters
    {
        // Send any characters the bluetooth prints to the serial monitor
        Serial.print((char)bluetooth.read());
    }
    while(Serial.available() > 0)  // If stuff was typed in the serial monitor
    {
        bluetooth.print((char)Serial.read());
    }
    if (digitalRead(baud_rate_pin) == HIGH) {
        switch_baud_rate();
    }
    if (digitalRead(config_pin) == HIGH) {
        apply_config();
    }
    // and loop forever and ever!
}
