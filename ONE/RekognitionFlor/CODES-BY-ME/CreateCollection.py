import json
import boto3

rekognition = boto3.client('rekognition')
region = 'us-east-1'

def lambda_handler(event, context):
    response = rekognition.create_collection(
        CollectionId='kyle-collection3',
        Tags={
            'Name': 'kyle'        
        }
    )
    print("*****    AWS REKOGNITION HAS BEEN CREATED A NEW COLLECTION   *****")
    list_id = rekognition.list_collections(
    MaxResults=1
    )
    for id in list_id['CollectionIds']:
        ids = id
        print(id)
    