
import time
from optparse import OptionParser
import dream_cheeky

parser = OptionParser()
opts, args = parser.parse_args()

turret = dream_cheeky.Turret(opts)


def move_n_seconds(move_fn, n_seconds=2.0):
    print move_fn
    move_fn()
    time.sleep(n_seconds)
    turret.launcher.turretStop()
    print "done"


if __name__ == "__main__":
    from bottle import route, run

    @route('/hello')
    def hello():
        return "Hello World!"

    @route('/left')
    def left():
        print "Left"
        move_n_seconds(turret.launcher.turretLeft)
        return "Left"

    @route('/right')
    def right():
        print "Right"
        move_n_seconds(turret.launcher.turretRight)
        return "Right"

    @route('/down')
    def down():
        print "Down"
        move_n_seconds(turret.launcher.turretDown)
        return "Down"

    @route('/up')
    def up():
        print "Up"
        move_n_seconds(turret.launcher.turretUp)
        return "Up"

    @route('/stop')
    def stop():
        print "Stop"
        turret.launcher.turretStop()
        return "Stop"

    @route('/fire')
    def fire():
        print "Fire"
        turret.launcher.turretFire()
        return "Fire"

    run(host='0.0.0.0', port=8080, debug=True)



# def move_n_seconds(move_fn, n_seconds=8.0):
#     print move_fn
#     move_fn()
#     time.sleep(n_seconds)
#     turret.launcher.turretStop()
#     print "done"


# import sys
# cmd = sys.argv[1]
# print cmd.strip()

# if cmd == "fire":
#     turret.launcher.turretFire()

# elif cmd == "right":
#     move_n_seconds(turret.launcher.turretRight)

# elif cmd == "left":
#     move_n_seconds(turret.launcher.turretLeft)

# elif cmd == "down":
#     move_n_seconds(turret.launcher.turretDown)

# elif cmd == "up":
#     move_n_seconds(turret.launcher.turretUp)

# elif cmd == "stop":
#     turret.launcher.turretStop()


