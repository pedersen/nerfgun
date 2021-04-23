#!/usr/bin/python3
#
# thanhle Bluetooth keyboard/Mouse emulator DBUS Service
#

import logging
import os
import socket
import sys
logging.basicConfig(level=logging.DEBUG)

import bluetooth
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop


from btemu import constants


class BTKbDevice():
    MY_ADDRESS = bluetooth.read_local_bdaddr()
    MY_DEV_NAME = constants.DEV_NAME

    # define some constants

    def __init__(self):
        logging.debug("2. Setting up BT device")
        self.init_bt_device()
        self.init_bluez_profile()

    # configure the bluetooth hardware device
    def init_bt_device(self):
        logging.debug("3. Configuring Device name " + BTKbDevice.MY_DEV_NAME)
        # set the device class to a keybord and set the name
        os.system("hciconfig hci0 up")
        os.system("hciconfig hci0 class 0x0025C0")
        os.system("hciconfig hci0 name " + BTKbDevice.MY_DEV_NAME)
        # make the device discoverable
        os.system("hciconfig hci0 piscan")

    # set up a bluez profile to advertise device capabilities from a loaded service record
    def init_bluez_profile(self):
        logging.debug("4. Configuring Bluez Profile")
        # setup profile options
        service_record = constants.sdp_record
        opts = {
            "AutoConnect": True,
            "ServiceRecord": service_record
        }
        # retrieve a proxy for the bluez profile interface
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")
        manager.RegisterProfile("/org/bluez/hci0", constants.UUID, opts)
        logging.debug("6. Profile registered ")

    # listen for incoming client connections
    def listen(self):
        logging.debug("\033[0;33m7. Waiting for connections\033[0m")
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)  # BluetoothSocket(L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)  # BluetoothSocket(L2CAP)
        self.scontrol.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sinterrupt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind these sockets to a port - port zero to select next available
        self.scontrol.bind((socket.BDADDR_ANY, constants.P_CTRL))
        self.sinterrupt.bind((socket.BDADDR_ANY, constants.P_INTR))

        # Start listening on the server sockets
        self.scontrol.listen(5)
        self.sinterrupt.listen(5)

        self.ccontrol, cinfo = self.scontrol.accept()
        logging.debug ("\033[0;32mGot a connection on the control channel from %s \033[0m" % cinfo[0])

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        logging.debug ("\033[0;32mGot a connection on the interrupt channel from %s \033[0m" % cinfo[0])

    # send a string to the bluetooth host machine
    def send_string(self, message):
        try:
            self.cinterrupt.send(bytes(message))
        except OSError as err:
            logging.error(err)


class BTKbService(dbus.service.Object):

    def __init__(self):
        logging.debug("1. Setting up service")
        # set up as a dbus service
        bus_name = dbus.service.BusName("org.thanhle.btkbservice", bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, "/org/thanhle/btkbservice")
        # create and setup our device
        self.device = BTKbDevice()
        # start listening for connections
        self.device.listen()

    @dbus.service.method('org.thanhle.btkbservice', in_signature='yay')
    def send_keys(self, modifier_byte, keys):
        logging.debug("Get send_keys request through dbus")
        logging.debug("key msg: ", keys)
        state = [ 0xA1, 1, 0, 0, 0, 0, 0, 0, 0, 0 ]
        state[2] = int(modifier_byte)
        count = 4
        for key_code in keys:
            if(count < 10):
                state[count] = int(key_code)
            count += 1
        self.device.send_string(state)

    @dbus.service.method('org.thanhle.btkbservice', in_signature='yay')
    def send_mouse(self, modifier_byte, keys):
        state = [0xA1, 2, 0, 0, 0, 0]
        count = 2
        for key_code in keys:
            if(count < 6):
                state[count] = int(key_code)
            count += 1
        self.device.send_string(state)


# main routine
if __name__ == "__main__":
    # we can only run as root
    try:
        if not os.geteuid() == 0:
            sys.exit("Only root can run this script")

        DBusGMainLoop(set_as_default=True)
        myservice = BTKbService()
        loop = GLib.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        sys.exit()
