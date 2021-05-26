import logging
import logging.config
import sys
from optparse import OptionParser

import dbus
import dbus.service
import dbus.mainloop.glib
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from . import constants
from .agent_helpers import set_trusted
from .cfg import BtConfig
from .rootcheck import rootcheck
from .state import BtState


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
            BtState().loop.quit()

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        logging.info(f"Authorize {device} - {uuid}")

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        logging.debug(f"RequestPinCode {device}")
        set_trusted(device)
        return "0000"

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        logging.debug(f"RequestPinCode (device)")
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
        logging.info(f"Requesting Confirmation - {device} - {passkey}")
        set_trusted(device)

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        logging.debug(f"RequestAuthorization ({device})")

    @dbus.service.method(constants.AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        logging.debug("Cancel")


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
        app.agent = Agent(app.bus, constants.AGENT_PATH)
        app.agent.set_exit_on_release(False)
        obj = app.bus.get_object(constants.BUS_NAME, constants.BUS_NAME_PATH)
        app.manager = dbus.Interface(obj, constants.AGENT_MANAGER)
        app.manager.RegisterAgent(constants.AGENT_PATH, constants.CAPABILITY)
        app.manager.RequestDefaultAgent(constants.AGENT_PATH)
        logging.debug("Agent registered")

        app.loop = GLib.MainLoop()
        app.loop.run()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
