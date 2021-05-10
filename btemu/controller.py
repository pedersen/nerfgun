import logging
logging.basicConfig(level=logging.DEBUG)

import sys
import time
from dataclasses import dataclass
from optparse import OptionParser

import RPi.GPIO as GPIO
from . import constants
from .cfg import BtConfig
from .kbd import Keyboard
from .mouse import MouseClient
from .rootcheck import rootcheck


@dataclass
class PinState:
    pinnum: int
    state: int
    transition: float
    code: int
    key: str


def mainloop(keys, mods, mouse, cycle, mouse_repeat):
    now = time.time()

    keypins = [PinState(x, GPIO.LOW, now, keys[x], x) for x in keys.keys()]
    modpins = [PinState(x, GPIO.LOW, now, mods[x], x) for x in mods.keys()]
    mousepins = [PinState(x, GPIO.LOW, now, mouse[x], x) for x in mouse.keys()]

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for pin in keys.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for pin in mouse.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    keyboard = Keyboard()
    pointer = MouseClient()

    logging.info("Polling mouse and keyboard events")
    while True:
        now = time.time()
        downkeys = []
        for pin in modpins:
            state = GPIO.input(pin.pinnum)
            if state == GPIO.HIGH:
                keycode = constants.codemods[pin.code]
                keyboard.state[2][pin.code] = 1
                downkeys.append(constants.keytable[keycode])
            else:
                keyboard.state[2][pin.code] = 0
            if state != pin.state:
                pin.state = state
                pin.transition = now

        for pin in keypins:
            state = GPIO.input(pin.pinnum)
            if state != pin.state:
                if state == GPIO.HIGH:
                    downkeys.append(pin.code)
                else:
                    keyboard.send_key_up()
                pin.state = state
                pin.transition = now

        downkeys.extend([0, 0, 0, 0, 0, 0])
        for idx in range(0, 6):
            keyboard.state[4+idx] = downkeys[idx]

        keyboard.send_key_state()

        for pin in mousepins:
            # TODO: Fix up using the 9-DOF sensor once new soldering iron arrives
            state = GPIO.input(pin.pinnum)
            if state != pin.state:
                if state == GPIO.HIGH:
                    pointer.state[0] = pin.code
                else:
                    pointer.state[0] = 0
                pin.state = state
                pin.transition = now
                pointer.send_current()
            if (state == GPIO.HIGH) and (pin.transition + mouse_repeat) <= now:
                pointer.state[0] = 0
                pointer.send_current()
                pointer.state[0] = pin.code
                pointer.send_current()
                pin.transition = now
        time.sleep(cycle)

def main():
    rootcheck()
    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="filename",
                      help="path of config file to use", metavar="FILE")
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

        mainloop(keys, mods, mouse, cycle, mouse_repeat)
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
