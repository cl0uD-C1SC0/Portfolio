import json
import urllib
import boto3
import json
import time
print('Loading function')

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
ddb = boto3.client('dynamodb')


def get_labels(key, bucket):
    response = rekognition.detect_labels(
        Image={
            'S3Object':{'Bucket':bucket,'Name':key}
        },
        MinConfidence=50
    )
    raw_labels = response['Labels']
    top_five=[]
    for x in range(0,5):
        top_five.append(raw_labels[x]['Name'])

    return top_five

def get_Celebrities(key, bucket):
    response = rekognition.recognize_celebrities(
        Image={
           'S3Object':{'Bucket':bucket,'Name':key}
        }
    )
    Celebritie=[]

    for celebrity in response['CelebrityFaces']:
        #print ("Name: " + str(celebrity['Name']))
        #print ("celebrity: {:.2f}".format(celebrity['Face']['Confidence']))
        #print ("Position:")
        #print ("   Left: {:.2f}".format(celebrity['Face']['BoundingBox']['Height']))
        #print ("   Top: {:.2f}".format(celebrity['Face']['BoundingBox']['Top']))

        Celebritie.append(celebrity['Name'])
        Celebritie.append(celebrity['Face']['Confidence'])
        Celebritie.append(celebrity['Face']['BoundingBox']['Height'])
        Celebritie.append(celebrity['Face']['BoundingBox']['Top'])
    return Celebritie

def ddb_molding(key, messeage):
    label_list = ['label_1', 'label_2', 'label_3', 'label_4', 'label_5']
    return_message = {}
    return_message["image"] = {
        "S": str(key)
    }
    for i, label in enumerate(messeage):
        return_message[str(label_list[i])] = {
            "S": str(messeage[i])
        }
    return return_message

def ddb_celebrity_molding(ddb_json, messeage):
    label_list = ['Name', 'Confidence', 'BoundingBox_Height', 'BoundingBox_Top']
    return_message = ddb_json
    for i, label in enumerate(messeage):
        return_message[str(label_list[i])] = {
            "S": str(messeage[i])
        }
    return return_message

def ddb_input(table, data):
    ddb.put_item(TableName = table, Item = data)
    return

def lambda_handler(event, context):
    print(json.dumps(event))
    s3_message = event
    key = s3_message['Records'][0]['s3']['object']['key']
    bucket = s3_message['Records'][0]['s3']['bucket']['name']
    proceed = get_labels(key, bucket)


    if proceed:
        ddb_json = ddb_molding(key, proceed)
        if "Face" in proceed:
            Celebrity = get_Celebrities(key, bucket)
            ddb_json = ddb_celebrity_molding(ddb_json, Celebrity)
    else:
        pass

    print(json.dumps(ddb_json))
    #print(json.dumps(Celebrity))

    ddb_input("myrekognition", ddb_json)

    print("end")
