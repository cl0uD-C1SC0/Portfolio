import json
import boto3
import os

# Setting clients for project
ec2 = boto3.client('ec2')
sns = boto3.client('sns')
ec2_resource = boto3.resource('ec2')
#
# Setting region for project
#
region = 'us-east-1'
#
# Setting environment variables for project
arn = os.environ['arn']
isolated_sg = os.environ['isolated_sg']
instance = os.environ['instance_id']
sns_topic = os.environ['sns_topic']
# 
# The code bellow it's for change security group by instanceID searched in event
# inside of EventBridge
"""
instanceID = event["detail"]["resource"]["instanceDetails"]["InstanceId"]
if instanceID == os.environ['INSTANCE_ID']:
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instanceID)
    instance.modify_attribute(Groups[security_groupid])
"""

def lambda_handler(event, context):
    """
        This code put IAM Profile role in Infected EC2 Instance, and
        change then security group for an security group Isolated
    """
    # Putting a IAM Profile role for SSM
    ssm = ec2.associate_iam_instance_profile(
        IamInstanceProfile={
                'Arn': arn,
                'Name': 'EC2-InstanceProfile'
        },
        InstanceId=instance
    )
    respose = "Error"
    # Change security group for Isolated security group.
    instance2 = ec2_resource.Instance(instance)
    instance2.modify_attribute(Groups=[isolated_sg])
    
    #Sending an EMAIL
    response = "GuardDuty Remediation | - An EC2 has been infected and moved to Isolated Security Group - Please Verify this e-mail and instance by checkin in Session Manager."
    publish = sns.publish(
        TopicArn=sns_topic,
        Message=response
    )
    return publish