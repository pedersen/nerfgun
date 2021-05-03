#!/usr/bin/env bash

set -x
set -e

sudo raspi-config nonint do_expand_rootfs
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_serial 1 0
sudo raspi-config nonint set_config_var enable_uart 1 /boot/config.txt
sudo raspi-config nonint do_change_locale en_US.UTF-8
sudo raspi-config nonint do_change_timezone US/Eastern
sudo raspi-config nonint do_configure_keyboard us
sudo raspi-config nonint do_hostname nerfgun

sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-dev python3-smbus python3-pip python3-rpi.gpio git
sudo apt clean
sudo update-alternatives --install $(which python) python $(which $(readlink $(which python2))) 1
sudo update-alternatives --install $(which python) python $(which $(readlink $(which python3))) 2
sudo update-alternatives --auto python

sudo apt install -y bluez bluez-tools bluez-firmware libbluetooth-dev
sudo apt install -y python3-dbus python3-pyudev python3-evdev python3-gi
sudo pip3 install pybluez

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
test -d Adafruit_Python_BNO055 || git clone https://github.com/adafruit/Adafruit_Python_BNO055.git
cd Adafruit_Python_BNO055
sudo python setup.py install

cd ${SCRIPT_DIR}
test -d nerfgun || git clone https://github.com/pedersen/nerfgun.git
cd nerfgun
sudo python setup.py install
sudo cp sysconfigs/btemu-power.service /lib/systemd/system/btemu-power.service
sudo cp sysconfigs/org.thanhle.btkbservice.conf /etc/dbus-1/system.d
sudo cp sysconfigs/bluetooth.service /lib/systemd/system/bluetooth.service

sudo systemctl enable btemu-power
sudo systemctl restart btemu-power
sudo systemctl daemon-reload
sudo systemctl restart bluetooth

sudo shutdown -r now
