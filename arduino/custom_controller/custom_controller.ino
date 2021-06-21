#include <SoftwareSerial.h>

// https://bitbucket.org/bperrybap/openglcd/wiki/Home
#include <openGLCD.h>
#include <Adafruit_BNO055.h>

#include "keyboard.h"

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

const int loopdelay = 8;  // number of milliseconds for main loop to run, used to calculate how long to sleep when exiting main loop
unsigned long previousMillis = 0;  // will store last time loop was run, start with 0 for when the system starts up
long int loops = 0;  // number of times loop() has been called
const int refreshdelay = 250;  // number of milliseconds between screen refreshes
unsigned long previousRefreshMillis = 0;  // last milli that the display was refreshed, to limit how often we try to update the screen

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

typedef void (*Operation)(uint8_t);
typedef struct {
    uint8_t number;
    Operation op;
    byte code;
    unsigned long transition;
    byte state;
} input_pin;

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

void switch_baud_rate(uint8_t code) {
    Serial.println("Switching baud rate");
    bluetooth.begin(init_baudrate);
    start_command_mode();
    send_command("U," + running_baudrate_str + ",N", "Changing baudrate to " + running_baudrate_str);
    bluetooth.begin(running_baudrate);
    delay(cmd_delay);
    end_command_mode();
}

void apply_config(uint8_t code) {
    Serial.println("Applying bluetooth config");
    start_command_mode();
    send_command("SM,6", "Switch to Pairing Mode (vs Slave, Master, DTR)");
    send_command("SO,%", "Print out CONNECT/DISCONNECT messages for debugging");
    send_command("SH,0033", "Set HID flags to be keyboard/combo mouse");
    send_command("S~,6", "Switch to HID mode");
    send_command("SN," + device_name, "Set device name");
    send_command("SQ,16", "Switch to low latency mode");
    send_command("R,1", "Reboot", 5);
    switch_baud_rate(0);
    Serial.println("Settings applied, bluetooth rebooted");
}

void send_key(uint8_t code) {

}
void send_modifier(uint8_t code) {

}
void send_button(uint8_t code) {

}
void send_mouse(uint8_t code) {

}

input_pin keypins[] = {
        {baud_rate_pin, switch_baud_rate, KEY_RESERVED, 0, LOW},
        {config_pin, apply_config, KEY_RESERVED, 0, LOW},
};
input_pin modpins[] = {

};
input_pin mouse_buttons[] = {

};

void setup() {
    Serial.begin(serial_baud_rate);  // Begin the serial monitor at 9600bps
    switch_baud_rate(0);
    for (auto & keypin : keypins) {
        pinMode(keypin.number, INPUT);
        keypin.transition = 0;
    }
    Serial.println("Initializing Display");
    GLCD.Init();   // initialise the library, non inverted writes pixels onto a clear screen
    GLCD.ClearScreen();
    GLCD.SelectFont(System5x7); // default fixed width system font
    /* Initialise the sensor */
    if (!bno.begin()) {
        /* There was a problem detecting the BNO055 ... check your connections */
        GLCD.DrawString("No BNO055 detected", 3, 3);
        while (true);
    }

    // load sensor calibration data if it exists
    /* Functions to deal with raw calibration data */
//    bool getSensorOffsets(uint8_t *calibData);
//    bool getSensorOffsets(adafruit_bno055_offsets_t &offsets_type);
//    void setSensorOffsets(const uint8_t *calibData);
//    void setSensorOffsets(const adafruit_bno055_offsets_t &offsets_type);
//    bool isFullyCalibrated();

    Serial.println("setup complete!");
}

void loop() {
    // don't do anything if we haven't had enough time pass
    unsigned long currentmillis = millis();
    if ((currentmillis - previousMillis) < loopdelay) {
        return; // not enough time has passed, and we are limiting ourselves to run once every loopdelay ms
    }
    previousMillis = currentmillis;
    loops ++;
    // don't update the display if we haven't had enough time pass
    if ((currentmillis - previousRefreshMillis) >= refreshdelay) {
        uint8_t system, gyro, accel, mag = 0;
        bno.getCalibration(&system, &gyro, &accel, &mag);

        char calibration[44];
        sprintf(calibration, "S:%d G:%d A:%d M:%d", system, gyro, accel, mag);
        char tstr[44];
        sprintf(tstr, "Ms:%lu", currentmillis);
        GLCD.DrawString(calibration, 0, 0, eraseFULL_LINE);
        GLCD.DrawString(tstr, 0, 8, eraseFULL_LINE);
        previousRefreshMillis = currentmillis;

        double seconds = currentmillis / 1000.0;
        int loops_per_second = int(loops / seconds);
        char loops_str[20];
        sprintf(loops_str, "Loops: %lu", loops);
        GLCD.DrawString(loops_str, 0, 16, eraseFULL_LINE);
        char loops_per_second_str[20];
        sprintf(loops_per_second_str, "Loops/Second: %d", loops_per_second);
        GLCD.DrawString(loops_per_second_str, 0, 24, eraseFULL_LINE);
    }


    // pass any serial traffic over the USB Serial for debugging
    while (bluetooth.available() > 0) { // If the bluetooth sent any characters
        Serial.print((char) bluetooth.read());
    }
    while (Serial.available() > 0) { // If stuff was typed in the serial monitor
        bluetooth.print((char) Serial.read());
    }

    // read key status and send key events
    // read imu and send mouse motion events / mouse click events
    // update display as needed
    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);

    for (auto & keypin : keypins) {
        if (digitalRead(keypin.number) == HIGH) {
            keypin.op(keypin.code);
        }
    }
    /*
    # get position at start to ensure relative positioning
    speed = Point(1, 1, 1)
    origin = Point(*bno.read_euler())
    now = time.time()

    keypins = [PinState(pin, GPIO.LOW, now, key) for (pin, key) in keycfgs.items()]
    modpins = [PinState(pin, GPIO.LOW, now, key) for (pin, key) in modcfgs.items()]
    mousepins = [PinState(pin, GPIO.LOW, now, key) for (pin, key) in mouse.items()]

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in keycfgs.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for pin in mouse.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(powerpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    keyboard = KeyboardClient()
    mouse = MouseClient()

    logging.info("Polling mouse and keyboard events")
    while True:
        now = time.time()
        state = GPIO.input(powerpin)
        if state == GPIO.HIGH:
            subprocess.call(['shutdown', '-h', 'now'], shell=False)

        for pin in modpins:
            state = GPIO.input(pin.pinnum)
            if state == GPIO.HIGH:
                keyboard.mod_key_down(pin.key)
                keyboard.key_down(pin.key)
            else:
                keyboard.mod_key_up(pin.key)
                keyboard.key_up(pin.key)
            if state != pin.state:
                pin.state = state
                pin.transition = now

        for pin in keypins:
            state = GPIO.input(pin.pinnum)
            if state != pin.state:
                if state == GPIO.HIGH:
                    keyboard.key_down(pin.key)
                else:
                    keyboard.key_up(pin.key)
                pin.state = state
                pin.transition = now

        keyboard.send_key_state()

        current = Point(*bno.read_euler())
        diff = (origin - current) * speed
        minshift = 0.5
        if abs(diff.x) > minshift:
            mouse.dx = diff.degree_to_byte(diff.x)
        if abs(diff.y) > minshift:
            mouse.dy = diff.degree_to_byte(diff.y)
        if abs(diff.z) > minshift:
            mouse.dz = diff.degree_to_byte(diff.z)

        for pin in mousepins:
            state = GPIO.input(pin.pinnum)
            if state != pin.state:
                if state == GPIO.HIGH:
                    mouse.button_down(int(pin.key))
                else:
                    mouse.button_up()
                pin.state = state
                pin.transition = now
                mouse.send()
            if (state == GPIO.HIGH) and (pin.transition + mouse_repeat) <= now:
                # mouse button up
                mouse.button_up()
                mouse.send()
                # mouse button down
                time.sleep(constants.KEY_DELAY)
                mouse.button_down(int(pin.key))
                mouse.send()
                pin.transition = now

        mouse.send()

        sys, gyro, accel, mag = bno.get_calibration_status()
        draw.text((x, top), f"Sys {sys} Gyro {gyro} Acc {accel} Mag {mag}", font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(cycle)
     */
}
