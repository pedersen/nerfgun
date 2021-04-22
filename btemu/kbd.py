#
# https://thanhle.me/make-raspberry-pi3-as-an-emulator-bluetooth-keyboard/
#
#
#
# Convert value returned from Linux event device ("evdev") to a HID code. This
# is reverse of what's actually hardcoded in the kernel.
#
# Thanh Le <quangthanh010290@gmail.com>
# License: GPL
#
# Ported to a Python module by Thanh Le

import sys  # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time

from . import constants


class InvalidKeyCode(Exception):
    pass


def convert(evdev_keycode):
    try:
        return constants.keytable[evdev_keycode]
    except KeyError:
        raise InvalidKeyCode(evdev_keycode)


def scancode(key):
    return constants.keytable[f"KEY_{key.upper()}"]


def modkey(evdev_keycode):
    return constants.modkeys.get(evdev_keycode, -1)


class Keyboard:
    def __init__(self):
        # the structure for a bt keyboard input report (size is 10 bytes)
        self.state = [
            0xA1,  # this is an input report
            0x01,  # Usage report = Keyboard
            # Bit array for Modifier keys
            [0,  # Right GUI - Windows Key
             0,  # Right ALT
             0,  # Right Shift
             0,  # Right Control
             0,  # Left GUI
             0,  # Left ALT
             0,  # Left Shift
             0],  # Left Control
            0x00,  # Vendor reserved
            0x00,  # rest is space for 6 keys
            0x00,
            0x00,
            0x00,
            0x00,
            0x00]
        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object('org.thanhle.btkbservice', '/org/thanhle/btkbservice')
        self.iface = dbus.Interface(self.btkservice, 'org.thanhle.btkbservice')

    def send_key_state(self):
        """sends a single frame of the current key state to the emulator server"""
        bin_str = ""
        element = self.state[2]
        for bit in element:
            bin_str += str(bit)
        self.iface.send_keys(int(bin_str, 2), self.state[4:10])

    def send_key_down(self, scancode):
        """sends a key down event to the server"""
        self.state[4] = scancode
        self.send_key_state()

    def send_key_up(self):
        """sends a key up event to the server"""
        self.state[4] = 0
        self.send_key_state()

    def send_string(self, string_to_send):
        string_to_send = string_to_send.upper()
        for c in string_to_send:
            self.send_key_down(scancode(c))
            time.sleep(constants.KEY_DOWN_TIME)
            self.send_key_up()
            time.sleep(constants.KEY_DELAY)


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Usage: send_string <string to send>")
        sys.exit(1)
    dc = Keyboard()
    for s in sys.argv[1:]:
        print("Sending " + s)
        dc.send_string(s)
        print("Done.")
