import logging
logging.basicConfig(level=logging.DEBUG)

import sys
import dbus
from optparse import OptionParser

from .rootcheck import rootcheck


class MouseClient():
	def __init__(self):
		self.state = [0, 0, 0, 0]
		self.bus = dbus.SystemBus()
		self.btkservice = self.bus.get_object('org.thanhle.btkbservice', '/org/thanhle/btkbservice')
		self.iface = dbus.Interface(self.btkservice, 'org.thanhle.btkbservice')

	def send_current(self):
		try:
			self.iface.send_mouse(0, bytes(self.state))
		except OSError as err:
			logging.error(err)


def main():
	rootcheck()
	parser = OptionParser("usage: %prog button_num dx dy dz")
	(opts, args) = parser.parse_args()
	if len(args) != 4:
		logging.error("must supplu: button_num dx dy dz")
		parser.print_help()
		exit()
	client = MouseClient()
	client.state[0] = int(sys.argv[1])
	client.state[1] = int(sys.argv[2])
	client.state[2] = int(sys.argv[3])
	client.state[3] = int(sys.argv[4])
	logging.debug(f"state: {client.state}")
	client.send_current()


if __name__ == "__main__":
	main()