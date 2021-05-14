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

## Software Preparation

* Start by getting Raspbian Lite installed and accessible on an SD card of at least 8GB.
  Use the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to do so.
* On the newly created boot partition, take the following steps:
  1. Create an empty file named `ssh`.
  2. Create a file named `wpa_supplicant.conf` with the following contents:
      ```
      ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
      country=US
      network={
        ssid="WFiNetworkName"
        psk="WiFiPassword"
      }
      ```
      Modify the country code to match your country.
  3. Put [the install script](https://raw.githubusercontent.com/pedersen/nerfgun/main/install.sh)
     into here as well.
* If you are on Windows, install [Bonjour Print Services](https://support.apple.com/kb/dl999?locale=en_US).
* If you are on Linux, install [Avahi Daemon](http://avahi.org/). On Debian/Ubuntu and derivatives,
  `sudo apt install -y avahi-daemon avahi-dnsconfd avahi-utils`.
* Install the SD card into the Raspberry Pi and boot it up.
* Once it is installed, ssh into `pi@raspberrypi.local`. On Windows, use
  [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) to do so.
* Run `bash /boot/install.sh`. Wait about 40 minutes, and everything will be ready.
