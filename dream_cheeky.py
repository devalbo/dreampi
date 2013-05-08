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

    # turn off turret properly
    def dispose(self):
        self.launcher.turretStop()
        turret.launcher.ledOff()

    # roughly centers the turret
    def center(self):
        print 'Centering camera ...'

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

    # adjusts the turret's position (units are fairly arbitary but work ok)
    def adjust(self, right_dist, down_dist):
        right_seconds = right_dist * 0.64
        down_seconds = down_dist * 0.48

        if right_seconds > 0:
            self.launcher.turretRight()
            time.sleep(right_seconds)
            self.launcher.turretStop()
        elif right_seconds < 0:
            self.launcher.turretLeft()
            time.sleep(- right_seconds)
            self.launcher.turretStop()

        if down_seconds > 0:
            self.launcher.turretDown()
            time.sleep(down_seconds)
            self.launcher.turretStop()
        elif down_seconds < 0:
            self.launcher.turretUp()
            time.sleep(- down_seconds)
            self.launcher.turretStop()

        # OpenCV takes pictures VERY quickly, so if we use it (Windows and OS X), we must
        # add an artificial delay to reduce camera wobble and improve clarity
        if sys.platform == 'win32' or sys.platform == 'darwin':
            time.sleep(.2)

    #stores images of the targets within the killcam folder
    def killcam(self, camera):
        # create killcam dir if none exists, then find first unused filename
        if not os.path.exists("killcam"):
            os.makedirs("killcam")
        filename_locked_on = os.path.join("killcam", "lockedon" + str(self.killcam_count) + ".jpg")
        while os.path.exists(filename_locked_on):
            self.killcam_count += 1
            filename_locked_on = os.path.join("killcam", "lockedon" + str(self.killcam_count) + ".jpg")

        # save the image with the target being locked on
        shutil.copyfile(self.opts.processed_img_file, filename_locked_on)

        # wait a little bit to attempt to catch the target's reaction.
        time.sleep(1)  # tweak this value for most hilarious action shots

        # take another picture of the target while it is being fired upon
        filename_firing = os.path.join("killcam", "firing" + str(self.killcam_count) + ".jpg")
        camera.capture()
        camera.face_detect(filename=filename_firing)

        self.killcam_count += 1

    # compensate vertically for distance to target
    def projectile_compensation(self, target_y_size):
        if target_y_size != 0:
            # objects further away will need a greater adjustment to hit target
            adjust_amount = 0.1 * math.log(target_y_size)
        else:
            # log 0 will throw an error, so handle this case even though unlikely to occur
            adjust_amount = 0

        # tilt the turret up to try to increase range
        self.adjust(0, adjust_amount)
        if opts.verbose:
            print "size of target: %.6f" % target_y_size
            print "compensation amount: %.6f" % adjust_amount

    # turn on LED if face detected in range, and fire missiles if armed
    def ready_aim_fire(self, x_adj, y_adj, target_y_size, camera=None):
        fired = False
        if face_detected and abs(x_adj) < .05 and abs(y_adj) < .05:
            turret.launcher.ledOn()  # LED will turn on when target is locked
            if self.opts.armed:
                # aim a little higher if our target is in the distance
                self.projectile_compensation(target_y_size)

                turret.launcher.turretFire()
                self.missiles_remaining -= 1
                fired = True

                if camera:
                    self.killcam(camera)  # save a picture of the target

                time.sleep(3)  # disable turret for approximate time required to fire

                print 'Missile fired! Estimated ' + str(self.missiles_remaining) + ' missiles remaining.'

                if self.missiles_remaining < 1:
                    raw_input("Ammunition depleted. Awaiting order to continue assault. [ENTER]")
                    self.missiles_remaining = 4
            else:
                print 'Turret trained but not firing because of the --disarm directive.'
        else:
            turret.launcher.ledOff()
        return fired



if __name__ == '__main__':
    if (sys.platform == 'linux2' or sys.platform == 'darwin') and not os.geteuid() == 0:
        sys.exit("Script must be run as root.")

    # command-line options
    parser = OptionParser()
    parser.add_option("-d", "--disarm", action="store_false", dest="armed", default=True,
                      help="track faces but do not fire any missiles")
    parser.add_option("-r", "--reset", action="store_true", dest="reset_only", default=False,
                      help="reset the turret position and exit")
    parser.add_option("--nd", "--no-display", action="store_true", dest="no_display", default=False,
                      help="do not display captured images")
    parser.add_option("-c", "--camera", dest="camera", default='0',
                      help="specify the camera # to use. Default: 0", metavar="NUM")
    parser.add_option("-s", "--size", dest="image_dimensions", default='320x240',
                      help="image dimensions (recommended: 320x240 or 640x480). Default: 320x240",
                      metavar="WIDTHxHEIGHT")
    parser.add_option("-b", "--buffer", dest="buffer_size", type="int", default=2,
                      help="size of camera buffer. Default: 2", metavar="SIZE")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="detailed output, including timing information")
    opts, args = parser.parse_args()
    print opts

    # additional options
    opts = AttributeDict(vars(opts))  # converting opts to an AttributeDict so we can add extra options
    opts.haar_file = 'haarcascade_frontalface_default.xml'
    opts.processed_img_file = 'capture_faces.jpg'

    turret = Turret(opts)

    if not opts.reset_only:
        while True:
            try:
                start_time = time.time()

                camera.capture()
                capture_time = time.time()

                face_detected, x_adj, y_adj, face_y_size = camera.face_detect()
                detection_time = time.time()

                if not opts.no_display:
                    camera.display()

                if face_detected:
                    if opts.verbose:
                        print "adjusting turret: x=" + str(x_adj) + ", y=" + str(y_adj)
                    turret.adjust(x_adj, y_adj)
                movement_time = time.time()

                if opts.verbose:
                    print "capture time: " + str(capture_time - start_time)
                    print "detection time: " + str(detection_time - capture_time)
                    print "movement time: " + str(movement_time - detection_time)

                turret.ready_aim_fire(x_adj, y_adj, face_y_size, camera)

            except KeyboardInterrupt:
                turret.dispose()
                camera.dispose()
                break
