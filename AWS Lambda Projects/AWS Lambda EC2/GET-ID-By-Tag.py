import boto3
region = 'us-east-1'
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):

    # Esse código pega o ID da Instância pela TAG Key, Key=Start, Value=Qualquerum
    # Troque o valor intance-type para tag-key ou tag:nomedaKeytag

    instances_id = ''
    print('Into DescribeEc2Instance')
    instances = ec2.describe_instances(Filters=[{'Name': 'instance-type', 'Values': [t2.micro, t3.micro]}])
    for ins_id in instances['Reservations'][0]['Instances']:
        instances_id = ins_id['InstanceId']
        print(instances_id)