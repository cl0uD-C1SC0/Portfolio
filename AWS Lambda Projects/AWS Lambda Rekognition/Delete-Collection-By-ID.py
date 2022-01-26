import json
import boto3

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
region = 'us-east-1'

def lambda_handler(event, context):
    """
       Esse código ele vai deletar os ID's que foram pegos
       no collection_get_id.
       Podemos também selecionar quantos ID's podemos deletar
       trocando os valores do MaxResults de 100 para 1 por exemplo.

       Código criado por: José Gabriel
    """
    collection_get_id = rekognition_client.list_collections(
        MaxResults=100
    )
    id_getted = ""
    id_out = []
    for id in collection_get_id['CollectionIds']:
        id_getted = id
        id_out.append(id)
        items = len(id_out)
        while items > 0:
                delete_collection_by_id = rekognition_client.delete_collection(
                    CollectionId=id_getted
                    )
                print("Deleting Collection ID: ", id_getted)
                break
    if id_getted == "":
        print("Don't have Collection ID's to delete")

    """
        Código mais simples para essa function:
    """
    """
        collection_get_id = rekognition_client.list_collections(
        MaxResults=100
    )
    for id in collection_get_id['CollectionIds']:
        delete_collection_by_id = rekognition_client.delete_collection(
            CollectionId=id
        )
        if id == "":
            print("Don't have Collection ID's to delete")
        else:
            print("Deleting Collection ID: ", id)
    """