#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.DEBUG)

import subprocess
import sys
from optparse import OptionParser

import RPi.GPIO as GPIO
from btemu.cfg import BtConfig
from btemu.rootcheck import rootcheck


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
        powerpin = cfg.powerpin
        logging.info(f"GPIO Power Pin is {powerpin}")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(powerpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.wait_for_edge(powerpin, GPIO.FALLING)

        subprocess.call(['shutdown', '-h', 'now'], shell=False)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
