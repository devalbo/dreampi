
import os
import time
from optparse import OptionParser
import dream_cheeky

parser = OptionParser()
opts, args = parser.parse_args()

turret = dream_cheeky.Turret(opts)

current_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.abspath(os.path.join(current_dir, "static"))


def move_n_seconds(move_fn, n_seconds=0.5):
    print move_fn
    move_fn()
    time.sleep(n_seconds)
    turret.launcher.turretStop()
    print "done"


from flask import Flask, redirect, send_file
app = Flask(__name__)

@app.route('/')
def index():
    return send_file("index.html")

@app.route('/left', methods=['POST'])
def left():
    move_n_seconds(turret.launcher.turretLeft)
    return redirect('/')

@app.route('/right', methods=['POST'])
def right():
    move_n_seconds(turret.launcher.turretRight)
    return redirect('/')

@app.route('/down', methods=['POST'])
def down():
    move_n_seconds(turret.launcher.turretDown)
    return redirect('/')

@app.route('/up', methods=['POST'])
def up():
    move_n_seconds(turret.launcher.turretUp)
    return redirect('/')

@app.route('/stop', methods=['POST'])
def stop():
    turret.launcher.turretStop()
    return redirect('/')

@app.route('/fire', methods=['POST'])
def fire():
    turret.launcher.turretFire()
    return redirect('/')

app.run(host='0.0.0.0',
        port=8080,
        debug=False)
