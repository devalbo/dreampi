#!/bin/bash

# on Raspbian, put this file in /etc/init.d, then run 'chmod a+x /etc/init.d/start-dreampi.sh', then 'update-rc.d start-dreampi.sh defaults'

cd /home/pi/Projects/dreampi
sudo venv/bin/python flask_operate.py
