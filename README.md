dreampi
=======

Want to run a Dream Cheeky USB foam dart launcher off of a Raspberry Pi over a webpage? So do I. Here's how I'm doing
it...

* Get a Raspberry Pi running Raspbian
* Get your Python development tools set up (assuming a fresh install)
  - Run 'sudo apt-get install python-pip'
  - Run 'sudo pip install virtualenv'
* Make sure you have git installed on your Raspberry Pi (if you don't, run 'sudo apt-get install git')
* Git clone the repo onto your Raspberry Pi - run 'git clone https://github.com/devalbo/dreampi'
* Navigate into the cloned dreampi directory (cd dreampi)
* Run 'virtualenv venv' to set up a new virtual environment
* Run source venv/bin/activate
* Run 'pip install -r requirements.txt'
* Run 'python operate.py'
* Open a browser and navigate to your Raspberry Pi's IP address and port 8080 (e.g. http://192.168.0.11:8080) to start
operating your Dream Cheeky launcher

Inspiration and software based on this blog post: https://github.com/AlexNisnevich/sentinel
