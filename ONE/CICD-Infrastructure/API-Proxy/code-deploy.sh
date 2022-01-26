#!/bin/bash
cd /home/ec2-user
pip3 install -r requirements.txt
killall python3
nohup python3 app.py &>/dev/null &
