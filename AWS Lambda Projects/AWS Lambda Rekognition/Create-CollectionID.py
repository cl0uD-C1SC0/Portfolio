import json
import boto3

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
region = 'us-east-1'

def lambda_handler(event, context):
    """
        Esse código cria uma nova coleção no AWS Rekognition
        Collection: Serve para guardar imagens para o Rekognition
        Treinar e poder utilizar as imagens treinadas para serem
        comparadas

        Código criado por: José Gabriel
    """

    CollectionId = ''
    print("***** AWS REKOGNITION: CREATING A NEW COLLECTION *****")
    collection = rekognition_client.create_collection(
        CollectionId='kyle-collection',
        Tags={
          'kyle': 'event'
        }
    )
    collection_get_id = rekognition_client.list_collections(
        MaxResults=100
    )
    for id in collection_get_id['CollectionIds']:
        print("***** AWS REKOGNITION: CREATED A NEW COLLECTION *****")
        print(id)