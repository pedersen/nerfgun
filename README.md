---
title: NerfGun Game Controller
keywords:
  -
...

# Inspiration

This project was inspired by the work of Alfredo Sequeida to make a [Nerf Gun into a
controller for Call of Duty](https://github.com/AlfredoSequeida/Nerf-Gun-Call-of-Duty-Warzone-Controller).

The project is amazingly cool. I love what I see, I just think it could stand some
improvements. In particular, I take issue with the following:

* Motion detection is done via an Android phone, dumping the data into a Raspberry Pi.
  High battery requirements, noticeable extra weight, and even then it requires some
  specialized understanding (roll the Nerf rifle to turn, instead of turning).
* Uses a Raspberry Pi 4. High power draw, which means a big battery to power it. That
  battery adds a lot of weight, which will help the gun itself feel a bit off.
* Uses TCP to connect to the host. While workable (as was obvious, since he could play
  the game), it does introduce higher latency in the controls.
* Platform specific, limited to Windows.
* Limited feedback on the Nerf controller itself. Difficult to debug what's happening
  inside.

Those are genuine functionality issues to address, and I think I have a decent solution.

* Switch to [Raspberry Pi Zero WH](https://www.adafruit.com/product/3708) (not the Pico,
  creating my own Bluetooth stack has no appeal at this time). Reduced power consumption,
  plus smaller form factor, will make installation inside of something else much easier.
* Use a [9-DOF Motion Detecting Sensor](https://www.adafruit.com/product/2472). It's
  extremely small, so fits inside of something more easily. Lower power consumption.
  Possibly most importantly, it tracks turns without having to roll the device. In fact,
  rolling is totally separate, resulting in more natural movement.
* Switch to Bluetooth for connectivity. This will allow me to get the ZeroWH to act
  as a Bluetooth keyboard and mouse. Doing so ends any platform limitations. This
  will work on Windows, Linux, and Mac. In future, I may even be able to get it to
  work with consoles.
* Add an [OLED display](https://www.adafruit.com/product/3527) to allow the ZeroWH to
  provide updates and instructions to the user directly.
* With much lower battery requirements, I can install a [Lithium Ion Polymer battery](https://www.adafruit.com/product/328)
  as well as a [USB Battery charging and device powering addon](https://www.adafruit.com/product/2465)
  to allow the device to be recharged as any other product on the market, and used
  without any more effort than any other device out there.
  
The ultimate plan here is to have a device where I've taken a [Nerf Fortnite AR-L](https://nerf.hasbro.com/en-us/product/fortnite-ar-l-nerf-elite-dart-blaster:BD9E4C78-1160-4FD6-9498-A39AC0632525)
and turned it into something that looks good, and plays comfortably. Getting there will
take some explanation. See [the installation](docs/install.md).

# Todo Items

* Have the controller reconnect when it's ready to begin use
* Turn on and start using the pioled display
* Modify setup.py to produce an actual installable package
* Create a GUI for managing the btemu.cfg file
* Enable "firmware updates" which will install a new version of the package
* Add potentiometers and ADCs to enable variable repeat speed for mouse clicks, walk speed
  (in keyboard mode)
* Add "Mouse Lock" key, which prevents the motion sensor from being used while it's depressed
  (useful for games which simulate such motion, or when needing to turn around 360, etc)
* Add controller mode which will allow to be connected as xbox/ps5/etc controller instead of
  keyboard/mouse