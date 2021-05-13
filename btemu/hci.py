#!/usr/bin/python3
"""
Bluetooth HID keyboard emulator DBUS Service

Original idea taken from:
http://yetanotherpointlesstechblog.blogspot.com/2016/04/emulating-bluetooth-keyboard-with.html

Moved to Python 3 and tested with BlueZ 5.43
"""
import logging
logging.basicConfig(level=logging.DEBUG)

import os
import socket
import subprocess
import sys
from optparse import OptionParser

import bluetooth
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

from . import constants
from .rootcheck import rootcheck
from .cfg import BtConfig

loop = None

class HumanInterfaceDeviceProfile(dbus.service.Object):
    """
    BlueZ D-Bus Profile for HID
    """
    fd = -1

    @dbus.service.method(constants.PROFILE, in_signature='', out_signature='')
    def Release(self):
        print('Release')
        loop.quit()

    @dbus.service.method(constants.PROFILE, in_signature='oha{sv}', out_signature='')
    def NewConnection(self, path, fd, properties):
        self.fd = fd.take()
        print('NewConnection({}, {})'.format(path, self.fd))
        for key in properties.keys():
            if key == 'Version' or key == 'Features':
                print('  {} = 0x{:04x}'.format(key, properties[key]))
            else:
                print('  {} = {}'.format(key, properties[key]))

    @dbus.service.method(constants.PROFILE, in_signature='o', out_signature='')
    def RequestDisconnection(self, path):
        print('RequestDisconnection {}'.format(path))

        if self.fd > 0:
            os.close(self.fd)
            self.fd = -1


class BTKbDevice:
    """
    create a bluetooth device to emulate a HID keyboard
    """
    # BlueZ dbus
    PROFILE_DBUS_PATH = constants.DBUS_PROFILE_PATH
    ADAPTER_IFACE = constants.ADAPTER_INTERFACE
    DEVICE_INTERFACE = constants.DEVICE_INTERFACE
    DBUS_PROP_IFACE = constants.DBUS_PROPERTIES
    DBUS_OM_IFACE = constants.DBUS_OBJECT_MANAGER

    def __init__(self, hci=0, dev_name=constants.DEV_NAME, p_ctrl=constants.P_CTRL, p_intr=constants.P_INTR):
        self.scontrol = None
        self.ccontrol = None  # Socket object for control
        self.sinterrupt = None
        self.cinterrupt = None  # Socket object for interrupt
        self.dev_path = '/org/bluez/hci{}'.format(hci)
        self.dev_name = dev_name
        self.P_INTR = p_intr
        self.P_CTRL = p_ctrl
        logging.info('Setting up BT device')
        self.bus = dbus.SystemBus()
        self.adapter_methods = dbus.Interface(self.bus.get_object(constants.BUS_NAME, self.dev_path),
                                              self.ADAPTER_IFACE)
        self.adapter_property = dbus.Interface(self.bus.get_object(constants.BUS_NAME, self.dev_path),
                                               self.DBUS_PROP_IFACE)

        self.bus.add_signal_receiver(self.interfaces_added, dbus_interface=self.DBUS_OM_IFACE,
                                     signal_name='InterfacesAdded')

        self.bus.add_signal_receiver(self._properties_changed, dbus_interface=self.DBUS_PROP_IFACE,
                                     signal_name='PropertiesChanged', arg0=self.DEVICE_INTERFACE, path_keyword='path')

        logging.info(f'Configuring for name {self.dev_name}')

        self.config_hid_profile()

        # set the Bluetooth device configuration
        self.alias = self.dev_name
        self.discoverabletimeout = 0
        self.discoverable = True

    def interfaces_added(self):
        pass

    def _properties_changed(self, interface, changed, invalidated, path):
        if self.on_disconnect is not None:
            if 'Connected' in changed:
                if not changed['Connected']:
                    self.on_disconnect()

    def on_disconnect(self):
        print('The client has been disconnected')
        self.listen()

    @property
    def address(self):
        """Return the adapter MAC address."""
        return self.adapter_property.Get(self.ADAPTER_IFACE, 'Address')

    @property
    def powered(self):
        """
        power state of the Adapter.
        """
        return self.adapter_property.Get(self.ADAPTER_IFACE, 'Powered')

    @powered.setter
    def powered(self, new_state):
        self.adapter_property.Set(self.ADAPTER_IFACE, 'Powered', new_state)

    @property
    def alias(self):
        return self.adapter_property.Get(self.ADAPTER_IFACE, 'Alias')

    @alias.setter
    def alias(self, new_alias):
        self.adapter_property.Set(self.ADAPTER_IFACE, 'Alias', new_alias)

    @property
    def discoverabletimeout(self):
        """Discoverable timeout of the Adapter."""
        return self.adapter_props.Get(self.ADAPTER_IFACE, 'DiscoverableTimeout')

    @discoverabletimeout.setter
    def discoverabletimeout(self, new_timeout):
        self.adapter_property.Set(self.ADAPTER_IFACE, 'DiscoverableTimeout', dbus.UInt32(new_timeout))

    @property
    def discoverable(self):
        """Discoverable state of the Adapter."""
        return self.adapter_props.Get(self.ADAPTER_INTERFACE, 'Discoverable')

    @discoverable.setter
    def discoverable(self, new_state):
        self.adapter_property.Set(self.ADAPTER_IFACE, 'Discoverable', new_state)

    def config_hid_profile(self):
        """
        Setup and register HID Profile
        """

        logging.info('Configuring Bluez Profile')

        opts = {
            'Role': 'server',
            'RequireAuthentication': False,
            'RequireAuthorization': False,
            'AutoConnect': True,
            'ServiceRecord': constants.sdp_record,
        }

        manager = dbus.Interface(self.bus.get_object(constants.BUS_NAME, constants.BUS_NAME_PATH),
                                 constants.PROFILE_MANAGER)

        HumanInterfaceDeviceProfile(self.bus, BTKbDevice.PROFILE_DBUS_PATH)

        manager.RegisterProfile(BTKbDevice.PROFILE_DBUS_PATH, constants.UUID, opts)

        logging.info('Profile registered ')

    def listen(self):
        """
        Listen for connections coming from HID client
        """

        print('Waiting for connections')
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.scontrol.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        self.sinterrupt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.scontrol.bind((self.address, self.P_CTRL))
        self.sinterrupt.bind((self.address, self.P_INTR))

        # Start listening on the server sockets
        self.scontrol.listen(1)  # Limit of 1 connection
        self.sinterrupt.listen(1)

        self.ccontrol, cinfo = self.scontrol.accept()
        logging.info(f'{cinfo[0]} connected on the control socket')

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print(f'{cinfo[0]} connected on the interrupt channel')

    def send(self, msg):
        """
        Send HID message
        :param msg: (bytes) HID packet to send
        """
        self.cinterrupt.send(bytes(bytearray(msg)))


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
        self.device = BTKbDevice() if btdevice is None else btdevice

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


def main():
    rootcheck()
    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="filename", help="path of config file to use", metavar="FILE")
    (options, args) = parser.parse_args()
    if not options.filename:
        logging.error("*** Must supply config file parameter!")
        parser.print_help()
        sys.exit(2)
    try:
        cfg = BtConfig(options.filename)
        DBusGMainLoop(set_as_default=True)
        btkbdevice = BTKbDevice(dev_name=cfg.devname) if cfg.devname else None
        myservice = BTKbService(btdevice=btkbdevice)
        global loop
        loop = GLib.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        sys.exit()


# main routine
if __name__ == "__main__":
    main()
#