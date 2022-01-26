#!/bin/bash
curl https://s3.dualstack.us-east-1.amazonaws.com/aws-xray-assets.us-east-1/xray-daemon/aws-xray-daemon-linux-3.x.zip -o xray.zip
unzip xray.zip
chmod +x xray 
nohup ./xray & #We just got the linux AWS X-ray daemon, and ran it, so we get some metrics
python app.py
