import boto3

ec2_client = boto3.client('ec2')
region = 'us-east-1'


# Timeout to 1 min 3 seconds
# Run with Scheduled Rule
# Add Destionations Target: AmazonCloudWatch logs, Amazon EC2

def lambda_handler(object, context)
    ec2 = boto3.resource('ec2', region_name='us-east-1')

    # Listar somente os volumes com 'unattached volume' (available)
    volumes = ec2.volumes.filter(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    for volume in volumes:
        v = ec2.Volume(volume.id)
        print("Deleting EBS volume: {}, Size: {} GiB".format(v.id, v.size))
        v.delete()