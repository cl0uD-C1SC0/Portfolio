#!/bin/bash

"""
sudo curl https://ee-assets-prod-us-east-1.s3.amazonaws.com/modules/dude_wheres_my_website/v3/unicorn_rentals_website_1_0.zip -o unicorn_rentals.zip
sudo unzip unicorn_rentals.zip
chmod +700 ./unicorentalswebserver.py
./unicorenrentalswebserver.py
"""
sudo yum update -y
sudo yum install -y python3 python3-pip python3-setuptools
sudo python3 -m pip install flask
sudo mkdir /website
cd /website

sudo curl https://ee-assets-prod-us-east-1.s3.amazonaws.com/modules/dude_wheres_my_website/v3/unicorn_rentals_website_1_0.zip -o unicorn_rentals.zip
sudo unzip unicorn_rentals.zip
chmod +700 ./unicornrentalswebserver.py
./unicorentalswebserver.py

