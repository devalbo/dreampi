
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
    
from flask import make_response
from functools import update_wrapper

def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)


from flask import Flask, redirect, send_file
app = Flask(__name__)

@app.route('/')
@nocache
def index():
    return send_file("index.html")

@app.route('/left', methods=['POST'])
@nocache
def left():
    move_n_seconds(turret.launcher.turretLeft)
    return redirect('/')

@app.route('/right', methods=['POST'])
@nocache
def right():
    move_n_seconds(turret.launcher.turretRight)
    return redirect('/')

@app.route('/down', methods=['POST'])
@nocache
def down():
    move_n_seconds(turret.launcher.turretDown)
    return redirect('/')

@app.route('/up', methods=['POST'])
@nocache
def up():
    move_n_seconds(turret.launcher.turretUp)
    return redirect('/')

@app.route('/stop', methods=['POST'])
@nocache
def stop():
    turret.launcher.turretStop()
    return redirect('/')

@app.route('/fire', methods=['POST'])
@nocache
def fire():
    turret.launcher.turretFire()
    return redirect('/')

app.run(host='0.0.0.0',
        port=8080,
        debug=False)
