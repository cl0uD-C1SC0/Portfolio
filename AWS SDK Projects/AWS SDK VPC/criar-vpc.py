import boto3
ec2 = boto3.resource('ec2')

# Criando a VPC

vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')

# nome para a vpc

vpc.create_tags(Tags=[{"Key": "Name", "Value": "VPC_WS31"}])
vpc.wait_until_available()

# Permitir DNS Hostanme e SSH.

ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute( VpcId = vpc.id, EnableDnsSupport = { 'Value': True } )
ec2Client.modify_vpc_attribute( VpcId = vpc.id, EnableDnsHostnames = { 'Value': True } )

# Criando um Internet Gateway.

internetgateway = ec2.create_internet_gateway()
internetgateway.create_tags(Tags=[{"Key": "Name", "Value": "InternetGateway44"}])
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)

# Criando uma route table.

routetable = vpc.create_route_table()
routetable.create_tags(Tags=[{"Key": "Name", "Value": "RouteTable-Pub24"}])
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)

# Criando subnets e associando a VPC.

subnet1apub = ec2.create_subnet(CidrBlock='10.0.0.0/24', VpcId=vpc.id, AvailabilityZone='us-east-1a')
subent2bpub = ec2.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc.id, AvailabilityZone='us-east-1b')
subnet3cpub = ec2.create_subnet(CidrBlock='10.0.2.0/24', VpcId=vpc.id, AvailabilityZone='us-east-1c')

# Nomeando as Subnets criadas

subnet1apub.create_tags(Tags=[{"Key": "Name", "Value": "Subnet-1a-Pub"}])
subent2bpub.create_tags(Tags=[{"Key": "Name", "Value": "Subnet-1b-Pub"}])
subnet3cpub.create_tags(Tags=[{"Key": "Name", "Value": "Subnet-1c-Pub"}])

# Associando as subnets criadas a routetable

routetable.associate_with_subnet(SubnetId=subnet1apub.id)
routetable.associate_with_subnet(SubnetId=subent2bpub.id)
routetable.associate_with_subnet(SubnetId=subnet3cpub.id)

subnet1apub = ec2Client.modify_subnet_attribute(
    MapPublicIpOnLaunch={
        'Value': True
    },
    SubnetId=subnet1apub.id
)

# Criando um Security Group para acesso via SSH.

SG_SSH = ec2.create_security_group(GroupName='SG-Only-SSH', Description='only allow SSH traffic', VpcId=vpc.id)
SG_SSH.create_tags(Tags=[{"Key": "Name", "Value": "SG-EC2"}])
SG_SSH.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)

