import logging
import os
import shutil
from importlib.resources import read_text
from subprocess import check_call

import btemu.resources


def write_resource(fname, resource_module, resource_name):
    logging.info(f'(Re)Creating {fname}')
    data = read_text(resource_module, resource_name)
    f = open(fname, 'w')
    f.write(data)
    f.close()


def main():
    logging.basicConfig(level=logging.DEBUG)
    if not os.path.exists('/etc/btemu'):
        os.makedirs('/etc/btemu')
    for (fname, rname) in [('/etc/btemu/btemu.conf', 'btemu.conf'),
                           ('/etc/btemu/btemu-logging.ini', 'btemu-logging.ini'),
                           ('/etc/dbus-1/system.d/org.thanhle.btkbservice.conf', 'org.thanhle.btkbservice.conf'),
                           ('/lib/systemd/system/btemu-hid.service', 'btemu-hid.service'),
                           ('/lib/systemd/system/btemu-agent.service', 'btemu-agent.service'),
                           ('/lib/systemd/system/bluetooth.service', 'bluetooth.service')]:
        write_resource(fname, btemu.resources, rname)

    if os.path.exists('/boot/btemu.conf'):
        logging.info('Found /boot/btemu.conf, installing it')
        shutil.copy('/boot/btemu.conf', '/etc/btemu/btemu.conf')

    logging.info('Reloading SystemD State')
    check_call(['systemctl', 'daemon-reload'])

    daemons = ['bluetooth', 'btemu-hid', 'btemu-agent']
    for daemon in daemons:
        logging.info(f'Enabling {daemon}')
        check_call(['systemctl', 'enable', daemon])
        logging.info(f'(Re)Starting {daemon}')
        check_call(['systemctl', 'restart', daemon])


if __name__ == '__main__':
    main()
