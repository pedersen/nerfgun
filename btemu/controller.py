import logging

import subprocess

logging.basicConfig(level=logging.DEBUG)

import sys
import time
from dataclasses import dataclass
from optparse import OptionParser

import RPi.GPIO as GPIO
from . import constants
from .cfg import BtConfig
from .kbd import KeyboardClient
from .mouse import MouseClient
from .rootcheck import rootcheck


@dataclass
class PinState:
    pinnum: int
    state: int
    transition: float
    key: str


def mainloop(keycfgs, modcfgs, mouse, cycle, mouse_repeat, powerpin):
    now = time.time()

    keypins = [PinState(pin, GPIO.LOW, now, key) for (pin, key) in keycfgs.items()]
    modpins = [PinState(pin, GPIO.LOW, now, key) for (pin, key) in modcfgs.items()]
    mousepins = [PinState(pin, GPIO.LOW, now, key) for (pin, key) in mouse.items()]

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
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

        for pin in mousepins:
            # TODO: Fix up using the 9-DOF sensor once new soldering iron arrives
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

        time.sleep(cycle)


def main():
    rootcheck()
    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="filename", help="path of config file to use", metavar="FILE",
                      default="/etc/btemu.conf")
    (options, args) = parser.parse_args()
    if not options.filename:
        logging.error("*** Must supply config file parameter!")
        parser.print_help()
        sys.exit(2)
    try:
        cfg = BtConfig(options.filename)
        keys, mods = cfg.keyboardpins
        mouse = cfg.mousepins
        cycle = cfg.cycle
        mouse_repeat = cfg.mouse_repeat
        powerpin = cfg.powerpin

        mainloop(keys, mods, mouse, cycle, mouse_repeat, powerpin)
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
