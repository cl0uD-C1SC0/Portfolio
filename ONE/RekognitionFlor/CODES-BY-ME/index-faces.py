#!/usr/bin/env python
"""
This is starter code to populate your Rekognition collection
After you populate your collection, you'll need another function to "detect Kyle" based on S3 uploads to your bucket.
"""
import boto3
import os 

######
# Getting our environment variables
# Make sure to set these in your lambda function
######
# the prepoopulated bucket containing our training images
bucket=os.environ['training_bucket']
# this is the name of the rekognition collection you've created
rekognition_collection_id = os.environ['collection']
# Rekognition allows you to specify a "tag" with your image.
# so later when we detect a matching face, we read this tag
# so we know the name or title of the person we've matched
external_image_id = 'Kyle'
region = 'us-east-1'
# create our respective service clients
s3_client=boto3.client('s3')
rekognition_client=boto3.client('rekognition')

def lambda_handler(event, context):
    """
    Main Lambda handler
    """
    
    # getting a list of all images in our bucket that we can iterate through
    response = s3_client.list_objects(
        Bucket='rekognition-trainning-bucket',
    )
 
    if 'Contents' in response:
        for obj in response['Contents']:
            file = obj['Key']
            index = rekognition_client.index_faces(
            CollectionId=rekognition_collection_id,
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': file
                }
            },
            ExternalImageId=external_image_id
        )
            return(index)
    else:
        print("No objects returned")
    
    for obj in resp['Contents']:
        print 'Object Name: %s' %obj['Key']