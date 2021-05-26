import logging
logging.basicConfig(level=logging.DEBUG)

import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from optparse import OptionParser
from typing import Tuple

import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from . import constants
from .adafruit import BNO055
from .adafruit import SSD1306
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


def displayoff(signum, frame):
    disp = SSD1306.SSD1306_128_32(rst=None)
    disp.clear()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(image)
    disp.display()
    sys.exit(0)


def rmap(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def degreemap(x: float) -> int:
    return int(rmap(x, 0, 360, -127, 126))


def spacemap(x: float, y: float, z: float) -> Tuple[int, int, int]:
    return -degreemap(x), -int(rmap(y, -90, 90, -127, 126)), degreemap(z)


def mainloop(keycfgs, modcfgs, mouse, cycle, mouse_repeat, powerpin):
    signal.signal(signal.SIGINT, displayoff)
    disp = SSD1306.SSD1306_128_32(rst=None)
    disp.begin()
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    font = ImageFont.truetype('DejaVuSansMono.ttf', 8)
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    # get position at start to ensure relative positioning
    heading, roll, pitch = bno.read_euler()
    cdx, cdy, cdz = spacemap(heading, roll, pitch)
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

        heading, roll, pitch = bno.read_euler()
        newcdx, newcdy, newcdz = spacemap(heading, roll, pitch)
        minshift = 5
        if abs(newcdx - cdx) > minshift:
            cdx = mouse.dx = newcdx
        else:
            mouse.dx = 0
        if abs(newcdy - cdy) > minshift:
            cdy = mouse.dy = newcdy
        else:
            mouse.dy = 0
        if abs(newcdz - cdz) > minshift:
            cdz = mouse.dz = newcdz
        else:
            mouse.dz = 0
        mouse.send()
        sys, gyro, accel, mag = bno.get_calibration_status()
        draw.text((x,top), f"Sys {sys} Gyro {gyro} Acc {accel} Mag {mag}", font=font, fill=255)
        disp.image(image)
        disp.display()
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
