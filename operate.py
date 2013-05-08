
import os
import time
from optparse import OptionParser
import dream_cheeky

parser = OptionParser()
opts, args = parser.parse_args()

turret = dream_cheeky.Turret(opts)

current_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.abspath(os.path.join(current_dir, "static"))


def move_n_seconds(move_fn, n_seconds=2.0):
    print move_fn
    move_fn()
    time.sleep(n_seconds)
    turret.launcher.turretStop()
    print "done"


if __name__ == "__main__":
    from bottle import route, run, static_file

    @route('/')
    def index():
        return static_file("index.html", root=current_dir)

    @route('/static/<filepath:path>')
    def server_static(filepath):
        return static_file(filepath, root=static_dir)

    @route('/left', method='POST')
    def left():
        print "Left"
        move_n_seconds(turret.launcher.turretLeft)
        return "Left"

    @route('/right', method='POST')
    def right():
        print "Right"
        move_n_seconds(turret.launcher.turretRight)
        return "Right"

    @route('/down', method='POST')
    def down():
        print "Down"
        move_n_seconds(turret.launcher.turretDown)
        return "Down"

    @route('/up', method='POST')
    def up():
        print "Up"
        move_n_seconds(turret.launcher.turretUp)
        return "Up"

    @route('/stop', method='POST')
    def stop():
        print "Stop"
        turret.launcher.turretStop()
        return "Stop"

    @route('/fire', method='POST')
    def fire():
        print "Fire"
        turret.launcher.turretFire()
        return "Fire"

    run(host='0.0.0.0', port=8080, debug=True)
