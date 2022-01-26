import json
import boto3
import time

region = 'us-east-1'
rds_client = boto3.client('rds')

def lambda_handler(event, context):
    snapshot = rds_client.create_db_snapshot(
        DBSnapshotIdentifier='snapshot-to-encrypt3',
        DBInstanceIdentifier='database-1',
        Tags=[{
            'Key': 'Name',
            'Value': 'snapshot-to-encrypt2'
            },
        ]
    )
    time.sleep(240)
    restore = rds_client.restore_db_cluster_from_snapshot(
        AvailabilityZones=[
            'us-east-1a'
            ],
        DBClusterIdentifier="new-database-1",
        SnapshotIdentifier='snapshot-to-encrypt3',
        DatabaseName="new-database-2",
        Engine='MySQL',
        DBClusterInstanceClas='db.t3.small'
    )
    time.sleep(360)
    return restore