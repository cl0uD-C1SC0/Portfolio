from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_iam as iam
from aws_cdk import aws_eks as eks
from aws_cdk import aws_ec2 as ec2
import aws_cdk.aws_eks

class ClusterStack(cdk.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        
        #VPC
        SubnetConfiguration = ec2.SubnetConfiguration

        vpc = ec2.Vpc(self, 'vpc-teste',
        cidr="10.0.0.0/16",
        max_azs=2,
        enable_dns_hostnames=True,
        enable_dns_support=True,
        subnet_configuration=[
            ec2.SubnetConfiguration(
                name='Public-Subnet-1a',
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24
            ),
            ec2.SubnetConfiguration(
                name='Private',
                subnet_type=ec2.SubnetType.PRIVATE,
                cidr_mask=24
            )
        ],
        nat_gateways=1
    )

    # Lookup up the default vpc 

        #vpc1 = ec2.Vpc.from_lookup(self, "VPC", vpc_id = "vpc-teste")

        # Create a master role for EKS Cluster

        iam_role = iam.Role(self, id=f"{id}-iam", role_name=f"{id}-iam", assumed_by=iam.AccountRootPrincipal())

        # Creating EKS Cluster with EKS
        eks_cluster = eks.Cluster(
            self, 
            id=f"{id}-cluster", 
            cluster_name=f"{id}-cluster", 
            vpc=vpc, 
            vpc_subnets=vpc.public_subnets, 
            masters_role=iam_role,  
            version=eks.KubernetesVersion.V1_20,
            )
        eks_cluster.add_nodegroup_capacity("extra-ng-spot",
            max_size=2,
            disk_size=20,
            instance_types=[
                ec2.InstanceType("t2.micro"),
            ],
        )

        # Creating Deployment and Service
        deployment = {
        apiVersion: "apps/v1",
        kind: "Deployment",
        metadata: { name: "hello-kubernetes" },
        spec: {
            replicas: 3,
            selector: { matchLabels: appLabel },
            template: {
            metadata: { labels: appLabel },
            spec: {
                containers: [
                {
                    name: "hello-kubernetes",
                    image: "paulbouwer/hello-kubernetes:1.5",
                    ports: [ { containerPort: 8080 } ]
                }
                ]
            }
            }
        }
        };

        service = {
        apiVersion: "v1",
        kind: "Service",
        metadata: { name: "hello-kubernetes" },
        spec: {
            type: "LoadBalancer",
            ports: [ { port: 80, targetPort: 8080 } ],
            selector: appLabel
        }
    };

        #// option 1: use a construct
        #new KubernetesManifest(this, 'hello-kub', {
        #cluster,
        #manifest: [ deployment, service ]
        #});
        
        
