import logging
import os

import dbus.service

from . import constants
from .state import BtState


class HumanInterfaceDeviceProfile(dbus.service.Object):
    """
    BlueZ D-Bus Profile for HID
    """
    fd = -1

    @dbus.service.method(constants.PROFILE, in_signature='', out_signature='')
    def Release(self):
        logging.info('Release')
        BtState().loop.quit()

    @dbus.service.method(constants.PROFILE, in_signature='oha{sv}', out_signature='')
    def NewConnection(self, path, fd, properties):
        self.fd = fd.take()
        logging.info(f'NewConnection({path}, {self.fd})')
        for key in properties.keys():
            if key == 'Version' or key == 'Features':
                logging.info(f'  {key} = 0x{properties[key]:04x}')
            else:
                logging.info(f'  {key} = {properties[key]}')

    @dbus.service.method(constants.PROFILE, in_signature='o', out_signature='')
    def RequestDisconnection(self, path):
        logging.info(f'RequestDisconnection {path}')

        if self.fd > 0:
            os.close(self.fd)
            self.fd = -1