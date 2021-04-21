---
title: Building From Scratch
keywords:
  - 
...

# Necessary Equipment

* [Nerf Fortnite AR-L](https://nerf.hasbro.com/en-us/product/fortnite-ar-l-nerf-elite-dart-blaster:BD9E4C78-1160-4FD6-9498-A39AC0632525)
* [Raspberry Pi Zero WH](https://www.adafruit.com/product/3708)
* [9-DOF Motion Detecting Sensor](https://www.adafruit.com/product/2472)
* [OLED display](https://www.adafruit.com/product/3527)
* [Lithium Ion Polymer battery](https://www.adafruit.com/product/328)
* [USB Battery charging and device powering addon](https://www.adafruit.com/product/2465)
* [A prototyping board](https://www.adafruit.com/product/571)
* Buttons, wires, solder, soldering iron, micro sd card for the OS, etc

# Installation Steps

## Initial Steps

* Start by getting Raspbian Lite installed and accessible.
* Perform any updates you need to before actually digging into the rest of this guide.

## Install 9-DOF Sensor

* [This guide](https://www.digikey.com/htmldatasheets/production/1833950/0/0/1/bno055-with-raspberry-pi-beaglebone-black.html)
  was extremely helpful, though it did have some inaccuracies three years later. In
  particular, you will need to take the following steps before actually beginning to
  work on the software:
  ```python
  sudo apt install -y python3-dev python3-smbus python3-pip python3-rpi.gpio
  sudo update-alternatives --install $(which python) python $(which $(readlink $(which python2))) 1
  sudo update-alternatives --install $(which python) python $(which $(readlink $(which python3))) 2
  sudo update-alternatives --config python
  ```
  Make sure to choose Python3 as your default version of Python. From there, you can
  follow the guide as presented, and get to the point where you can manipulate the
  animal statues in your web browser.
* You now have the 9-DOF sensor installed, working, and ready to go.

## Configure As Bluetooth Keyboard and Mouse

