
import boto3
import os
import cfnresponse
import json

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
              print "Deleting %s" % file['Key']
              client.delete_object(
                  Bucket=bucket,
                  Key=file['Key'],
              )

def send_response(event, context):
  responseData = {}
  cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalID")

def lambda_handler(event, context):
  print json.dumps(event)

  if event['RequestType'] == 'Create':
    # copying the training images to the player bucket
    for training_image in training_images:
        print "Copying %s" % training_image
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