#!/usr/bin/python3
"""
Bluetooth HID keyboard emulator DBUS Service

Original idea taken from:
http://yetanotherpointlesstechblog.blogspot.com/2016/04/emulating-bluetooth-keyboard-with.html

Moved to Python 3 and tested with BlueZ 5.43
"""
import logging
import logging.config
import sys
from optparse import OptionParser

import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

from . import constants
from .cfg import BtConfig
from .device import BtHidDevice
from .rootcheck import rootcheck
from .service import BTKbService
from .state import BtState


def main():
    rootcheck()
    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="filename", help="path of config file to use", metavar="FILE",
                      default="/etc/btemu/btemu.conf")
    (options, args) = parser.parse_args()
    if not options.filename:
        logging.error("*** Must supply config file parameter!")
        parser.print_help()
        sys.exit(2)
    try:
        app = BtState()
        app.cfg = BtConfig(options.filename)
        logging.config.fileConfig(app.cfg.logging)
        DBusGMainLoop(set_as_default=True)

        app.bus = dbus.SystemBus()
        obj = app.bus.get_object(constants.BUS_NAME, constants.BUS_NAME_PATH)
        app.manager = dbus.Interface(obj, constants.AGENT_MANAGER)
        app.bthiddevice = BtHidDevice(dev_name=app.cfg.devname) if app.cfg.devname else None
        app.myservice = BTKbService(btdevice=app.bthiddevice)
        app.loop = GLib.MainLoop()

        logging.info("Waiting for connections")
        app.loop.run()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
