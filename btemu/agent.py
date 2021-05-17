import logging
logging.basicConfig(level=logging.DEBUG)

from optparse import OptionParser

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject

from . import constants
from .rootcheck import rootcheck

bus = None
device_obj = None
dev_path = None
mainloop = None


def get_managed_objects():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object(constants.BUS_NAME, "/"), constants.DBUS_OBJECT_MANAGER)
    return manager.GetManagedObjects()


def find_adapter(pattern=None):
    return find_adapter_in_objects(get_managed_objects(), pattern)


def find_adapter_in_objects(objects, pattern=None):
    bus = dbus.SystemBus()
    for path, ifaces in objects.iteritems():
        adapter = ifaces.get(constants.ADAPTER_INTERFACE)
        if adapter is None:
            continue
        if not pattern or pattern == adapter["Address"] or \
                path.endswith(pattern):
            obj = bus.get_object(constants.BUS_NAME, path)
            return dbus.Interface(obj, constants.ADAPTER_INTERFACE)
    raise Exception("Bluetooth adapter not found")


def find_device(device_address, adapter_pattern=None):
    return find_device_in_objects(get_managed_objects(), device_address, adapter_pattern)


def find_device_in_objects(objects, device_address, adapter_pattern=None):
    bus = dbus.SystemBus()
    path_prefix = ""
    if adapter_pattern:
        adapter = find_adapter_in_objects(objects, adapter_pattern)
        path_prefix = adapter.object_path
    for path, ifaces in objects.iteritems():
        device = ifaces.get(constants.DEVICE_INTERFACE)
        if device is None:
            continue
        if (device["Address"] == device_address and
                path.startswith(path_prefix)):
            obj = bus.get_object(constants.BUS_NAME, path)
            return dbus.Interface(obj, constants.DEVICE_INTERFACE)

    raise Exception("Bluetooth device not found")


def set_trusted(path):
    props = dbus.Interface(bus.get_object(constants.BUS_NAME, path), constants.DBUS_PROPERTIES)
    props.Set(constants.DEVICE_INTERFACE, "Trusted", True)


def dev_connect(path):
    dev = dbus.Interface(bus.get_object(constants.BUS_NAME, path), constants.DEVICE_INTERFACE)
    dev.Connect()


class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


class Agent(dbus.service.Object):
    exit_on_release = True

    def set_exit_on_release(self, exit_on_release):
        self.exit_on_release = exit_on_release

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        logging.debug("Release")
        if self.exit_on_release:
            mainloop.quit()

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        return

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        logging.debug("RequestPinCode (%s)" % (device))
        set_trusted(device)
        return "0000"

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        set_trusted(device)
        return dbus.UInt32("000000")

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
        logging.debug(f"DisplayPasskey ({device}, {passkey:06} entered {entered:06})")

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="os", out_signature="")
    def DisplayPinCode(self, device, pincode):
        logging.debug(f"DisplayPinCode ({device}, {pincode})")

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        set_trusted(device)

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        logging.debug(f"RequestAuthorization ({device})")

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        logging.debug("Cancel")


def pair_reply():
    logging.debug("Device paired")
    set_trusted(dev_path)
    dev_connect(dev_path)
    mainloop.quit()


def pair_error(error):
    err_name = error.get_dbus_name()
    if err_name == "org.freedesktop.DBus.Error.NoReply" and device_obj:
        logging.debug("Timed out. Cancelling pairing")
        device_obj.CancelPairing()
    else:
        logging.debug(f"Creating device failed: {str(error)}")
    mainloop.quit()


def main():
    global mainloop, dev_path, device_obj
    rootcheck()

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    capability = "NoInputNoOutput"

    parser = OptionParser()
    parser.add_option("-i", "--adapter", action="store",
                      type="string",
                      dest="adapter_pattern",
                      default=None)
    parser.add_option("-c", "--capability", action="store",
                      type="string", dest="capability")
    parser.add_option("-t", "--timeout", action="store",
                      type="int", dest="timeout",
                      default=60000)
    (options, args) = parser.parse_args()
    if options.capability:
        capability = options.capability

    path = constants.AGENT_PATH
    agent = Agent(bus, path)

    mainloop = GObject.MainLoop()

    obj = bus.get_object(constants.BUS_NAME, constants.BUS_NAME_PATH)
    manager = dbus.Interface(obj, constants.AGENT_MANAGER)
    manager.RegisterAgent(path, capability)

    logging.debug("Agent registered")

    manager.RequestDefaultAgent(path)

    mainloop.run()


if __name__ == '__main__':
    main()
