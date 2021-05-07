import time
from dataclasses import dataclass
import RPi.GPIO as GPIO
from optparse import OptionParser

import sys

from btemu.cfg import BtConfig
from btemu.kbd import Keyboard
from btemu.mouse import MouseClient
from btemu.rootcheck import rootcheck


@dataclass
class PinState:
    pinnum: int
    state: int
    transition: float
    code: int


def mainloop(keys, mouse, cycle, mouse_repeat):
    now = time.time()

    keypins = [PinState(x, GPIO.PUD_DOWN, now, keys[x]) for x in keys.keys()]
    mousepins = [PinState(x, GPIO.PUD_DOWN, now, mouse[x]) for x in mouse.keys()]

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for pin in keys.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for pin in mouse.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    keyboard = Keyboard()
    pointer = MouseClient()

    while True:
        now = time.time()
        for pin in keypins:
            # TODO: Handle modifier keys properly
            state = GPIO.input(pin.pinnum)
            if state != pin.state:
                if state == GPIO.HIGH:
                    keyboard.send_key_down(pin.code)
                else:
                    keyboard.send_key_up()
                pin.state = state
                pin.transition = now

        for pin in mousepins:
            # TODO: Fix up auto-repeat of mouse clicks
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
            if state == GPIO.HIGH and now - mouse_repeat >= pin.transition:
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
        print(parser.usage)
        print("*** Must supply config file parameter!")
        sys.exit(2)
    try:
        cfg = BtConfig(options.filename)
        keys = cfg.keyboardpins
        mouse = cfg.mousepins
        cycle = cfg.cycle
        mouse_repeat = cfg.mouse_repeat

        mainloop(keys, mouse, cycle, mouse_repeat)
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
