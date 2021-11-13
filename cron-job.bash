#!/bin/bash    
cd /home/filipe/Documents/twitterbot
source venv/bin/activate

# virtualenv is now active, which means your PATH has been modified.
# Don't try to run python from /usr/bin/python, just run "python" and
# let the PATH figure out which version to run (based on what your
# virtualenv has configured).

python3 tweepy_favorites.py
deactivate