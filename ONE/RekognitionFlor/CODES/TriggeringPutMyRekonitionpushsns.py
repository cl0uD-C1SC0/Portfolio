import boto3
import json
import os
from datetime import datetime

# The SNSPublisher class publishes messages to SNS topics
ORDER_DETAILS = {"image": {"S": "matsuko5.jpg"}, "label_3": {"S": "Face"}}

# STUDENT TODO 2: Set ARN for SNS topic for order messages
TOPIC_ARN_ORDER = "arn:aws:sns:us-east-1:986846499074:relables"


snsTopic = 'arn:aws:sns:us-east-1:986846499074:relables'

name = 'relable'

sns = boto3.client('sns')
ddb = boto3.client('dynamodb')
def publish_order_msgs(orderDetails):
    topicArn=TOPIC_ARN_ORDER
    sns = boto3.resource('sns')
    publish_order(sns, topicArn, orderDetails)
    print("Order topic published")




def publish_order(sns, topic_arn, json_order):
    """Sends the order message

    Keyword arguments:
    sns -- SNS service resource
        topicArn -- ARN for the topic
        jsonStr -- the order in JSON format
    """

    topic = sns.Topic(topic_arn)
    topic.publish(Message=json_order)

def sent_message(msg):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=name)
    time = 1
    msg_list = [{'Id' : '{}'.format(time), 'MessageBody' : '\'image\': {0}'.format(msg)}]
    response = queue.send_messages(Entries=msg_list)
    print(response)
    return response


def querylabeltems(filter, value):

    response = ddb.query(
        TableName='myrekognition',
        KeyConditions={
            filter: {
                'AttributeValueList': [
                    {
                        'S': value
                    }
                ],
                'ComparisonOperator': "EQ"
            }
        }
    )
    return response

def lambda_handler(event, context):
    dynamo_message = event
    print(json.dumps(event))
#    NewImage = dynamo_message['Records'][0]['dynamodb']['NewImage'] #type dict
    Newkey = dynamo_message['Records'][0]['dynamodb']['Keys']['image']

    vulue = Newkey['S']

    NewImage = querylabeltems('image', vulue)

    responce = json.dumps(NewImage['Items'])

    responce = responce.lstrip('[')
    responce = responce.rstrip(']')
    json_responce = json.loads(responce)

    send_flag = False
    for y in json_responce:
        dep = json_responce[y]
        if (dep['S'] == 'Face'): #Face label ckeck
            print("find Face")
            send_flag = True
        else :
            pass

    if send_flag:
        #msg = dynamo_message['Records'][0]['dynamodb']['Keys']
        sent_message(json_responce['image']);
    else:
        pass
    print("Successfully")

