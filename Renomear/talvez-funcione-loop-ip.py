import json
import boto3
import os
import socket, struct
import ipaddress

vpc_client = boto3.client('ec2', region_name='us-east-1')


def lambda_handler(event, context):
#    cidr = socket.inet_aton(publicIp)

    cidr = event["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]['publicIp']
    print (cidr + '/' + '32')
    for ip in cidr:
        respons = vpc_client.create_network_acl_entry(
            CidrBlock = cidr + '/' + '32',
            Egress = True,
            NetworkAclId = 'acl-03047e3bbce6418c6',
            PortRange={
                'From': 22,
                'To': 22
            },
            Protocol = '6',
            RuleAction = 'allow',
            RuleNumber = 105
        )
        return respons