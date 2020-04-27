#!/bin/bash

source ./venv/bin/activate

python3 crawlers/2018playerstat.py;
python3 crawlers/2019kboteamstat.py;
python3 crawlers/2019playerstat.py;
crawlers/2019teamresult.py;

print "done."
