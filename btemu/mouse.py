import logging
import time

logging.basicConfig(level=logging.DEBUG)

import sys
import dbus
from optparse import OptionParser

from .rootcheck import rootcheck
from . import constants


class InvalidMouseButton(Exception):
    pass


class InvalidMouseMovement(Exception):
    pass


def twos_complement_byte(num):
    return int.from_bytes(int.to_bytes(num, 1, byteorder='big', signed=True), byteorder='big')


class MouseClient:
    """
    This class is responsible for generating DBUS mouse events. It takes instructions from outside, including when
    to send the events. Note that it does *not* determine what events should be sent, or in what order. It *only*
    manages the connection to the DBUS.
    """
    def __init__(self):
        self._dx = 0  # delta-x, must be signed byte (-128 to 127)
        self._dy = 0  # delta-y, must be signed byte (-128 to 127)
        self._dz = 0  # delta-z, must be signed byte (-128 to 127)
        self._button = 0  # button number, must be 0 to 127

        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object(constants.DBUS_DOTTED_NAME, constants.DBUS_PATH_NAME)
        self.iface = dbus.Interface(self.btkservice, constants.DBUS_DOTTED_NAME)

    @property
    def state(self):
        return bytes([self._button, self._dx, self._dy, self._dz])

    def send(self):
        try:
            self.iface.send_mouse(self.state)
        except OSError as err:
            logging.error(err)

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, buttonnum):
        if buttonnum < 0 or buttonnum > 127:
            raise InvalidMouseButton(f"button {buttonnum} not in range [0:127]")
        self._button = buttonnum

    def button_down(self, buttonnum):
        self.button = buttonnum

    def button_up(self):
        self.button = 0

    def button_click(self, buttonnum):
        self.button_down(buttonnum)
        self.send()
        time.sleep(constants.KEY_DELAY)
        self.button_up()
        self.send()

    @staticmethod
    def fix_range_delta(name, value):
        if value < -128 or value > 127:
            raise InvalidMouseMovement(f"{name} {value} not in range [-128:127]")
        return int.from_bytes(int.to_bytes(value, 1, byteorder='big', signed=True), byteorder='big')

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, dx):
        self._dx = self.fix_range_delta("dx", dx)

    @property
    def dy(self):
        return self._dy

    @dy.setter
    def dy(self, dy):
        self._dy = self.fix_range_delta("dy", dy)

    @property
    def dz(self):
        return self._dz

    @dz.setter
    def dz(self, dz):
        self._dz = self.fix_range_delta("dz", dz)


def main():
    rootcheck()
    parser = OptionParser("usage: %prog button_num dx dy dz")
    (opts, args) = parser.parse_args()
    if len(args) != 4:
        logging.error("must supply: button_num dx dy dz")
        parser.print_help()
        sys.exit(2)
    client = MouseClient()
    client.button = int(args[0])
    client.dx = int(args[1])
    client.dy = int(args[2])
    client.dz = int(args[3])
    logging.debug(f"button: {client.button}, dx: {client.dx}, dy: {client.dy}, dz: {client.dz}")
    client.send()


if __name__ == "__main__":
    main()
