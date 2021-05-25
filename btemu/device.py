import logging
import socket

import dbus

from . import constants
from .profile import HumanInterfaceDeviceProfile


class BtHidDevice:
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
        self.dev_path = f'{constants.BUS_NAME_PATH}/hci{hci}'
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

    def interfaces_added(self, path, interfaces):
        logging.info(f"path: {path} - interfaces: {str(interfaces)}")

    def _properties_changed(self, interface, changed, invalidated, path):
        if self.on_disconnect is not None:
            if 'Connected' in changed:
                if not changed['Connected']:
                    self.on_disconnect()

    def on_disconnect(self):
        logging.info('The client has been disconnected')
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

        HumanInterfaceDeviceProfile(self.bus, BtHidDevice.PROFILE_DBUS_PATH)

        manager.RegisterProfile(BtHidDevice.PROFILE_DBUS_PATH, constants.UUID, opts)

        logging.info('Profile registered ')

    def listen(self):
        """
        Listen for connections coming from HID client
        """

        logging.info('Waiting for connections')
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
        logging.info(f'{cinfo[0]} connected on the interrupt channel')

    def send(self, msg):
        """
        Send HID message
        :param msg: (bytes) HID packet to send
        """
        self.cinterrupt.send(bytes(bytearray(msg)))