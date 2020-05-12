#!/usr/bin/env bash
cd "${0%/*}"
CURRENTDATE=`date +"%Y-%m-%d %T"`
source venv/bin/activate
python main.py

echo "The shell script was successfully run at ${CURRENTDATE}" > shell-results.txt
