import boto3 

region = 'us-east-1'
ec2_client = boto3.client('ec2')

def lambda_handler(event, context):

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2 = boto3.client('ec2', region_name=region)

    response = ec2.describe_snapshots(OwnerIds=[account_id])
    snapshots = response['Snapshots']

    snapshots.sort(key-lambda x: x["StartTime"])

    snapshots = snapshots[:-3]

    for snapshot in snapshosts: 
        id = snapshot['SnapshotId']
        try:
            print("Deleting snapshot: ", id)
            ec2.delete_snapshot(SnapshotId=id)
        except Exception as e:
            if 'InvalidSnapshot.InUse' in e.message:
                print("Spashot {} in use, skipping.".format(id))
                continue