#!/bin/bash

REQUIREMENTS="requirements.txt"

rm -rf app
mkdir app

export PYTHONUSERBASE="app"
python3.8 -m pip install --upgrade --user -r $REQUIREMENTS --ignore-installed
unset PYTHONUSERBASE

mv app/lib/python/site-packages app/python
rm -r app/lib app/bin