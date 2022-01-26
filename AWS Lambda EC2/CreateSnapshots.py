import json
import boto3
from datetime import datetime

# This function create a snapshot of EBS Volume from
# EC2 instances with have tag key 'backup', with value 'true'

ec2_client = boto3.client('ec2')
region = 'us-east-1'

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name=region)
    
    instances = ec2.instances.filter(
        Filters=[{
            'Name': 'tag:backup', 'Values': ['true']}
        ]
    )
    
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
    
    for i in instances.all():
        for v in i.volumes.all():
            desc = 'Backup of {0}, volume {1}, created {2}'.format(
                i.id, v.id, timestamp)
            print(desc)
            
            snapshot = v.create_snapshot(Description=desc)
            
            print("Created snapshot: ", snapshot.id)
            