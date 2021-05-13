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

import logging
logging.basicConfig(level=logging.DEBUG)

import sys
import time
from optparse import OptionParser

import dbus
from . import constants
from .rootcheck import rootcheck


class TooManyKeys(Exception):
    pass


def scancode(key):
    if key == ' ':
        key = 'SPACE'
    return constants.keytable[f"KEY_{key.upper()}"]


class KeyboardClient:
    def __init__(self):
        # the structure for a bt keyboard input report (size is 10 bytes)
        self.modkeys = 0b00000000
        self.keys = []
        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object(constants.DBUS_DOTTED_NAME, constants.DBUS_PATH_NAME)
        self.iface = dbus.Interface(self.btkservice, constants.DBUS_DOTTED_NAME)

    def mod_key_down(self, modkey):
        key = constants.modkeys[f"KEY_{modkey}"]
        self.modkeys |= key

    def mod_key_up(self, modkey):
        key = constants.modkeys[f"KEY_{modkey}"]
        self.modkeys &= ~key

    def key_down(self, key):
        if len(self.keys) == 6:  # maximum number of keys bluetooth accepts
            raise TooManyKeys("Keyboard buffer overflow")
        self.keys.append(scancode(key))

    def key_up(self, key):
        key = scancode(key)
        if key in self.keys:
            self.keys.remove(key)

    def send_key_state(self):
        """sends a single frame of the current key state to the emulator server"""
        self.iface.send_keys(self.modkeys, bytes(self.keys))

    def send_key_down(self, key):
        """sends a key down event to the server"""
        self.key_down(key)
        self.send_key_state()

    def send_key_up(self, key):
        """sends a key up event to the server"""
        self.key_up(key)
        self.send_key_state()

    def send_string(self, string_to_send):
        string_to_send = string_to_send.upper()
        for c in string_to_send:
            self.send_key_down(c)
            time.sleep(constants.KEY_DOWN_TIME)
            self.send_key_up(c)
            time.sleep(constants.KEY_DELAY)


def main():
    rootcheck()
    parser = OptionParser(usage="usage: %prog string to send")
    (opts, args) = parser.parse_args()
    if len(args) == 0:
        logging.error("Must supply at least one string to send")
        parser.print_help()
        sys.exit(2)

    dc = KeyboardClient()
    for s in args:
        logging.info(f"Sending '{s}'")
        dc.send_string(s)
        dc.send_string(" ")
        logging.info("Done.")


if __name__ == "__main__":
    main()
