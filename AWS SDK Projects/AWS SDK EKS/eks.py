import boto3 

# Criando um IAM Policy:

#response = client.create_policy(
#    PolicyName='eksRoleName',
#    PolicyDocument=''
#    Description='Policy for EKS',
#    Tags=[
#        {
#            'Key': 'Name',
#            'Value': 'eksRolename'
#        },
#    ]
#)

# Criando uma IAM Role:

#response = client.create_role(
#    AssumeRolePolicyDOcument='string'
#    Path='/'
#    RoleName='eksRoleName'
#)


# Pegando um IAM Role Existente
iam = boto3.client('iam')
r = iam.get_role(RoleName="eksRoleName")
roleArn = r['Role']['Arn']

# Getting VPC ID, Subnet ID and the security Group ID
#cloudFormation = boto3.client('cloudformation')
#r = cloudFormation.describe_stack_resources(
#    StackName = "eks-vpc"
#    LogicalResource="VPC")
#vpcId = r['StackResources'][0]['PhysicalResourceId']
#r = cloudFormation.describe_stack_resources(
#   StackName = "eks-vpc",
#    LogicalResourceId="ControlPlaneSecurityGroup")
#secGroupid = r['StackResources'][0]['PhysicalResourceId']

eks = boto3.client("eks")
response = eks.create_cluster(
               name="myCluster",
               version="1.20",
               roleArn = roleArn,
               resourcesVpcConfig = {
                'subnetIds' : [
                    'subnet-00fb2c0aca0534e90','subnet-08a040a2a12515a57'
                ], 
                'securityGroupIds' : ["sg-0f9788664c340629d"]})
waiter = eks.get_waiter("cluster_active")
waiter.wait(name="myCluster")