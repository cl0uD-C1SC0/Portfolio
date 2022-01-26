
import boto3
import json
import os

rekognition_collection_id = os.environ['collection']
sns_topic_arn = os.environ['sns_arn']
team_id = os.environ['team_id']


external_image_id = 'Matsuko'

# our boto3 rekognition client
rekognition_client=boto3.client('rekognition')
sns_client=boto3.client('sns')

def facial_recognition(key, bucket):
    response = rekognition_client.index_faces(
        CollectionId=rekognition_collection_id,
        Image={
            'S3Object':{'Bucket':bucket,'Name':key}
        }
    )
    print ("Index Faces response:\n %s" % response)
    if not response['FaceRecords']:
        return False
    for face in response['FaceRecords']:
        face_id = face['Face']['FaceId']
        print ("Face ID: %s" % face_id)
        # send the detected face to Rekognition to see if it matches
        # anything in our collection
        response = rekognition_client.search_faces(
            CollectionId=rekognition_collection_id,
            FaceId=face_id,
            FaceMatchThreshold=50,
            MaxFaces=1
        )
        print ("Searching faces response:\n %s" % response)
        if not response['FaceMatches']:
            return False
        for match in response['FaceMatches']:
            if "ExternalImageId" in match['Face'] and match['Face']["ExternalImageId"] == external_image_id:

                print ("We've found our CEO!! Huzzah!")
                return True
        print ("not kyle :(")
        return False

def get_labels(key, bucket):
    response = rekognition_client.detect_labels(
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

def send_sns(message):

    print (message)
    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=(json.dumps(message)),
        #Message=u'message',
        Subject=u'subject'
    )

    return

def lambda_handler(event, context):

    print (json.dumps(event))
    s3_message = event
    key = s3_message['Records'][0]['s3']['object']['key']
    bucket = s3_message['Records'][0]['s3']['bucket']['name']
    proceed = facial_recognition(key, bucket)

    return_message={
        "key":key,
        "team_id":team_id
    }

    if proceed:
        labels = get_labels(key, bucket)
        return_message['labels']=labels
        return_message['kyle_present']=True
    else:
        return_message['kyle_present']=False

    send_sns(return_message)