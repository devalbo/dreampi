
import time
import dream_cheeky
from flask import Flask, redirect, send_file, make_response
from functools import update_wrapper

turret = dream_cheeky.Turret()
app = Flask(__name__)


def move_n_seconds(move_fn, n_seconds=0.5):
    print move_fn
    move_fn()
    time.sleep(n_seconds)
    turret.turretStop()
    print "done"


def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)

@app.route('/')
@nocache
def index():
    return send_file("index.html")

@app.route('/left', methods=['POST'])
@nocache
def left():
    move_n_seconds(turret.turretLeft)
    return redirect('/')

@app.route('/right', methods=['POST'])
@nocache
def right():
    move_n_seconds(turret.turretRight)
    return redirect('/')

@app.route('/down', methods=['POST'])
@nocache
def down():
    move_n_seconds(turret.turretDown)
    return redirect('/')

@app.route('/up', methods=['POST'])
@nocache
def up():
    move_n_seconds(turret.turretUp)
    return redirect('/')

@app.route('/stop', methods=['POST'])
@nocache
def stop():
    turret.turretStop()
    return redirect('/')

@app.route('/fire', methods=['POST'])
@nocache
def fire():
    turret.turretFire()
    return redirect('/')

app.run(host='0.0.0.0',
        port=8000,
        debug=False)
