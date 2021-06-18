#include <SoftwareSerial.h>

/*
 * openGLCD - https://bitbucket.org/bperrybap/openglcd/wiki/Home
 */

#include <openGLCD.h>
#include <Adafruit_BNO055.h>

const int serial_baud_rate = 9600;
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
const int refreshdelay = 250;  // number of milliseconds between screen refreshes
unsigned long previousRefreshMillis = 0;  // last milli that the display was refreshed, to limit how often we try to
// update the screen

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

gText textArea;

void start_command_mode(int multiplier = 1) {
    Serial.println("$$$ ::: Entering command mode");
    bluetooth.print("$$$");
    delay(cmd_delay * multiplier);
}

void send_command(String command, String message, int multiplier = 1) {
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

void setup() {
    Serial.begin(serial_baud_rate);  // Begin the serial monitor at 9600bps
    switch_baud_rate();
    pinMode(baud_rate_pin, INPUT);
    pinMode(config_pin, INPUT);
    Serial.println("Initializing Display");
    GLCD.Init();   // initialise the library, non inverted writes pixels onto a clear screen
    GLCD.ClearScreen();
    GLCD.SelectFont(System5x7); // default fixed width system font
    /* Initialise the sensor */
    if (!bno.begin()) {
        /* There was a problem detecting the BNO055 ... check your connections */
        GLCD.DrawString("No BNO055 detected", 3, 3);
        while (1);
    }

    Serial.println("setup complete!");
}

void loop() {
    unsigned long currentmillis = millis();
    if ((currentmillis - previousMillis) < loopdelay) {
        return; // not enough time has passed, and we are limiting ourselves to run once every loopdelay ms
    }
    previousMillis = currentmillis;
    if ((currentmillis - previousRefreshMillis) >= refreshdelay) {
        uint8_t system, gyro, accel, mag = 0;
        bno.getCalibration(&system, &gyro, &accel, &mag);

        char calibration[44];
        sprintf(calibration, "Sys:%d Gyr:%d Acc:%d Mag:%d Ms:%lu", system, gyro, accel, mag, currentmillis);
        GLCD.DrawString(calibration, 0, 0, eraseFULL_LINE);
        previousRefreshMillis = currentmillis;
    }
/*
    if (bluetooth.availableForWrite() == 0) {
        return;
    }
*/
    // read key status and send key events
    // read imu and send mouse motion events / mouse click events
    // update display as needed
    while (bluetooth.available() > 0)  // If the bluetooth sent any characters
    {
        // Send any characters the bluetooth prints to the serial monitor
        Serial.print((char) bluetooth.read());
    }
    while (Serial.available() > 0)  // If stuff was typed in the serial monitor
    {
        bluetooth.print((char) Serial.read());
    }
    if (digitalRead(baud_rate_pin) == HIGH) {
        switch_baud_rate();
    }
    if (digitalRead(config_pin) == HIGH) {
        apply_config();
    }
}
