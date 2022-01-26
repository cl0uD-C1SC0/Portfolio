import json
import boto3

reko = boto3.client('rekognition')

def lambda_handler(event, context):
    # TODO implement

    describe = rekognition.describe_collection(
        CollectionId='kyle-collection2'
        )
    return (json.dumps(describe, default=str))
