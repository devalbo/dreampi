#!/usr/bin/python

# SENTINEL
# A USB rocket launcher face-tracking solution
# For Linux and Windows
#
# Installation: see README.md
#
# Usage: sentinel.py [options]
#
# Options:
#   -h, --help            show this help message and exit
#   -d, --disarm          track faces but do not fire any missiles
#   -r, --reset           reset the turret position and exit
#   --nd, --no-display    do not display captured images
#   -c NUM, --camera=NUM  specify the camera # to use. Default: 0
#   -s WIDTHxHEIGHT, --size=WIDTHxHEIGHT
#                         image dimensions (recommended: 320x240 or 640x480).
#                         Default: 320x240
#   -b SIZE, --buffer=SIZE
#                         size of camera buffer. Default: 2
#   -v, --verbose         detailed output, including timing information

import os
import sys
import time
import usb.core
import subprocess
import shutil
import math
from optparse import OptionParser

# globals
FNULL = open(os.devnull, 'w')


# http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python
class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class LauncherDriver():
    # Low level launcher driver commands
    # this code mostly taken from https://github.com/nmilford/stormLauncher
    # with bits from https://github.com/codedance/Retaliation
    def __init__(self):
        self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.dev is None:
            raise ValueError('Missile launcher not found.')
        if sys.platform == 'linux2' and self.dev.is_kernel_driver_active(0) is True:
            self.dev.detach_kernel_driver(0)
        self.dev.set_configuration()

    def turretUp(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretDown(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretLeft(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretRight(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretStop(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretFire(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def ledOn(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def ledOff(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


class Turret():
    def __init__(self, opts):
        self.opts = opts
        self.launcher = LauncherDriver()
        self.missiles_remaining = 4
        
        # initial setup
        self.center()
        self.launcher.ledOff()
        self.cooldown_time = 3
        self.killcam_count = 0

    # roughly centers the turret
    def center(self):
        print 'Initializing turret ...'

        self.launcher.turretLeft()
        time.sleep(4)
        self.launcher.turretRight()
        time.sleep(2)
        self.launcher.turretStop()

        self.launcher.turretUp()
        time.sleep(1)
        self.launcher.turretDown()
        time.sleep(0.25)
        self.launcher.turretStop()
        print "Done centering..."