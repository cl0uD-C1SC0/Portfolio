# unicorn_api

This is our API Proxy code for use by trusted Unicorn Rentals partners, and less trusted DevOps teams. Its purpose is to proxy API calls to our backend. Every 4 minutes it uses a different auth secret to auth to the backend, and to validate the result with caller. Currently the auth is updated by a gitpush every 4 minutes.

## Architecture

Below was/is the proposed architecture for deploying this application. We have partially fulfilled the design in our MVP deployment.

![AWS Architecture](https://s3.amazonaws.com/gdengine-assets-staging.us-east-1/modules/casual_infrastructure_causes_disasters/player-assets/architecture.png)


## Getting Started

If you want to locally test etc:
* Have python 3.7  

This will deploy the python dependencies, and run a local web server.  

```
pip install -r requirements.txt
python app.py
```

## Tests
If deploying with CICD tooling, run tests via CodeBuild or any other CI tool.
```
python tests_app.py -v
```

Or you can manually test with cURL, httpie or a browser.

## Deployment

*__Configure AWS Parameter Store BACKEND_API value.__*

Then deploy how suits you, but we included an appspec.yml for AWS CodeDeploy.

Optionally have AWS xray deployed (executable not in this repo):
```
curl https://s3.dualstack.us-east-1.amazonaws.com/aws-xray-assets.us-east-1/xray-daemon/aws-xray-daemon-linux-3.x.zip -o xray.zip
unzip xray.zip
chmod +x xray 
nohup ./xray &
```

And have a default AWS region set, either via environment variable, or aws configure.

## Built With
Python  
Flask  
flask_restful  
Requests  
watchtower
