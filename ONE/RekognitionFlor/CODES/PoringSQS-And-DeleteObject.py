import json
import boto3

BUCKET_NAME = 'recognitoneventbacket'
TOPIC_ARN = 'arn:aws:sns:us-east-1:986846499074:mygmail'
msg = 'send test massage Hello hamasaki'
subject = 'test now!!'

def delete_objects(key):
    s3 = boto3.resource('s3')
    #s3.Bucket('recognitoneventbacket')
    #s3.delete_object(Bucket='bucket_name', Key=u'key')
    s3.Object('recognitoneventbacket', key).delete()
    return
def sent_email(key):
    sns = boto3.client('sns')

    request = {
        'TopicArn' : TOPIC_ARN,
        'Message' : 'Delete  ' + key + '!!',
        'Subject' : subject
    }
    response = sns.publish(**request)
    print('response')

def lambda_handler(event, context):
    sqs_message = event

    image_key = sqs_message['Records'][0]['body'] # Dictionary type is more convenient


    image = '{' + image_key + '}' # Format the string into json format  String type now!!
    iimage = image.replace('\'', '"') # Convert ' into " and format them into JSON format
    image = json.loads(iimage) # Load JSON format string as dictionary type
    #{'image': {'S': 'test2/matsuko.png'}}
    print(image['image']['S']) # test2/matsuko.png

    sent_email(image['image']['S'])

    delete_objects(image['image']['S'])

