import logging

import dbus

from . import constants
from .state import BtState

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
    bus = dbus.SystemBus()
    props = dbus.Interface(bus.get_object(constants.BUS_NAME, path), constants.DBUS_PROPERTIES)
    props.Set(constants.DEVICE_INTERFACE, "Trusted", True)


def dev_connect(path):
    bus = dbus.SystemBus()
    dev = dbus.Interface(bus.get_object(constants.BUS_NAME, path), constants.DEVICE_INTERFACE)
    dev.Connect()


def pair_reply():
    logging.debug("Device paired")
    app = BtState()
    set_trusted(app.dev_path)
    dev_connect(app.dev_path)


def pair_error(error):
    app = BtState()
    err_name = error.get_dbus_name()
    if err_name == "org.freedesktop.DBus.Error.NoReply" and app.device_obj:
        logging.debug("Timed out. Cancelling pairing")
        app.device_obj.CancelPairing()
    else:
        logging.debug(f"Creating device failed: {str(error)}")
