#
# Hey!! You're looking at the wrong spot. This function should be left alone, it's for the gameday internals.
# This function is used by the game itself. You have to CREATE A NEW ONE for identifying Kyle! RUN!!!
#
# Remember: AWS Documentation is your friend ;)
#

import boto3
import os
import json
import requests

# grabbing env vars
sourceBucket = os.environ['sourceBucket']
destBucket = os.environ['destBucket']
playerBucket = os.environ['playerBucket']
prefix = os.environ['prefix']

# setting up clients
s3 = boto3.resource('s3')
client = boto3.client('s3')

training_images = [
    'kyle_gameday.png',
    'kyle_linkedin.jpg',
    'kyle_phonetool.jpeg',
    'kyle_random1.jpg',
    'kyle_youtube1.png'
]


def send(event, context, responseStatus, responseData, reason=None, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    default_reason = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['Reason'] = reason or default_reason
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData
    json_responseBody = json.dumps(responseBody)
    print("Response body:\n" + json_responseBody)
    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }
    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

def deleteAll(bucket, prefix):
  paginator = client.get_paginator('list_objects')
  for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=prefix):
      # checking if there are nested folders
      if result.get('CommonPrefixes') is not None:
          for subdir in result.get('CommonPrefixes'):
              # delete files in the nested folders
              deleteAll(bucket, subdir['Prefix'])
      if result.get('Contents') is not None:
          for file in result.get('Contents'):
              print("Deleting %s" % file['Key'])
              client.delete_object(
                  Bucket=bucket,
                  Key=file['Key'],
              )

def send_response(event, context):
  responseData = {}
  send(event, context, "SUCCESS", responseData, "CustomResourcePhysicalID")

def lambda_handler(event, context):
  print(json.dumps(event))

  if event['RequestType'] == 'Create':
    # copying the training images to the player bucket
    for training_image in training_images:
        print("Copying %s" % training_image)
        copy_source = {
            'Bucket': sourceBucket,
            'Key': "{}{}".format(prefix, training_image)
        }
        s3.meta.client.copy(copy_source, destBucket, training_image)
    # now we signal back to CFN we're done
    send_response(event, context)
  if event['RequestType'] == 'Delete':
    # need to delete objects in the S3 bucket so the CFN stack
    # can delete the bucket
    deleteAll(destBucket,'')
    deleteAll(playerBucket,'')
    # now we signal back to CFN we're done
    send_response(event, context)
  if event['RequestType'] == 'Update':
    # now we signal back to CFN we're done
    send_response(event, context)