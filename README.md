# mushr-radio-controller
Using the BitCraze CrazyRadio to tele-operate the MuSHR racecar over radio (as opposed to normal WiFi/Bluetooth)

Currently using Logitech XInput, DualShock/alternative controller functionality TBA. 

## rx.py - run on receiving MuSHR Car
Receives controller data over CrazyRadio

Uses evdev to create a virtual XInput controller interfacing with ROS - joy.

## tx.py - run on transmitting PC
Requires inputs module & CrazyRadio device

Uses standard MuSHR Controls (L1 for DMS, joysticks for throttle and steering)

Press B to end radio transmission

## crazyradio.py
BitCraze CrazyRadio Python library (used under MIT License from BitCraze)
https://github.com/bitcraze/crazyradio-firmware

