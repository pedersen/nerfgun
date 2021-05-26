import logging

import dbus
import dbus.service

from . import constants
from .device import BtHidDevice


class BTKbService(dbus.service.Object):
    """
    Setup of a D-Bus service to recieve HID messages from other
    processes.
    Send the recieved HID messages to the Bluetooth HID server to send
    """
    def __init__(self, btdevice=None):
        logging.info('Setting up service')

        bus_name = dbus.service.BusName(constants.DBUS_DOTTED_NAME, bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, constants.DBUS_PATH_NAME)

        # create and setup our device
        self.device = BtHidDevice() if btdevice is None else btdevice

        # start listening for socket connections
        self.device.listen()

    @dbus.service.method(constants.DBUS_DOTTED_NAME, in_signature='yay')
    def send_keys(self, modifier_byte, cmd):
        state = [ constants.INPUT_REPORT,
                  constants.KBD_EVENT,
                  modifier_byte,
                  0,  # Vendor Reserved Byte
                  ]
        state.extend(cmd[:6])
        self.device.send(state)

    @dbus.service.method(constants.DBUS_DOTTED_NAME, in_signature='ay')
    def send_mouse(self, cmd):
        state = [ constants.INPUT_REPORT,
                  constants.MOUSE_EVENT,
                  ]
        state.extend(cmd)
        self.device.send(state)