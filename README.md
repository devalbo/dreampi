dreampi
=======

Want to run a <a target="_blank" href="http://www.amazon.com/s/?_encoding=UTF8&camp=1789&creative=390957&field-keywords=dream%20cheeky&linkCode=ur2&sprefix=dream%20chee%2Caps%2C165&tag=devalbo-20&url=search-alias%3Dtoys-and-games">Dream Cheeky USB foam dart launcher</a><img src="https://www.assoc-amazon.com/e/ir?t=devalbo-20&l=ur2&o=1" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />from a website hosted by a Raspberry Pi? So do I. Here's how I'm doing
it...

* Get a Raspberry Pi running Raspbian (see http://devalbo.blogspot.com/2013/03/first-steps.html)
* Plug the Dream Cheeky launcher into your Raspberry Pi
* Connect to your Raspberry Pi and open a terminal connection
* Make sure you're using the latest updates for Raspbian (run 'sudo apt-get update')
* Get your Python development tools set up (assuming a fresh install)
  - Run 'sudo apt-get install python-pip'
  - Run 'sudo pip install virtualenv'
* Make sure you have git installed on your Raspberry Pi (if you don't, run 'sudo apt-get install git')
* Git clone the repo onto your Raspberry Pi - run 'git clone https://github.com/devalbo/dreampi'
* Navigate into the cloned dreampi directory (run 'cd dreampi')
* Run 'virtualenv venv' to set up a new virtual environment
* Run 'source venv/bin/activate'
* Run 'pip install -r requirements.txt'
* There are two options to run; I prefer the flask option because the web-server performs better than bottle
  - Run 'python flask_operate.py' (better)
  - Run 'python operate.py'
* Open a browser and navigate to your Raspberry Pi's IP address (e.g. http://192.168.0.11) to start
operating your Dream Cheeky launcher

Inspiration and software based on this blog post: https://github.com/AlexNisnevich/sentinel
