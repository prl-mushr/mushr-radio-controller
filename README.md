# mushr-radio-controller
Using the BitCraze CrazyRadio to tele-operate the MuSHR racecar over radio (as opposed to normal WiFi/Bluetooth)

Use the XInput branch if you are using an Xbox or Logitech (in X-mode) controller. Use the main branch if you are using a DualShock 4 PS4 controller.

## rx.py - run on receiving MuSHR Car
Receives controller data over CrazyRadio

Uses evdev to create a virtual controller interfacing with ROS - joy. See file comments if you are using an unsupported controller and want to tweak the input to match your existing setup.

## tx.py - run on transmitting PC
Requires inputs module & CrazyRadio device

Uses standard MuSHR Controls (L1 for DMS, joysticks for throttle and steering), and communicates it over radio.

Press B to end radio transmission before terminating the script.

## crazyradio.py
BitCraze CrazyRadio Python library (used under MIT License from BitCraze)
https://github.com/bitcraze/crazyradio-firmware

