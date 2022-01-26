# Para criar a eks-demo-app-kubectl digite:
# No LINUX:
    ROLE="      - rolearn: arn:aws:iam::accountid:role/eks-demo-app-kubectl\n       username: build\n       groups:\n       -system:masters"

# Para criar o iam-role-policy digite:
# No LINUX:
    echo '{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": "eks:Describe", "Resource": "*"  } ] }' > /tmp/iam-role-policy

# 1 - Crie o TRUST:
# No LINUX:
    TRUST="{ \"Version\": \"2012-10-17"\, \"Statement\": [  { \"Effect\": \"Allow\", \"Principal\": { \"AWS\": \"arn:aws:iam::accountid:root\" }, \"Action\": \"sts:AssumeRole\" } ] }"

    aws iam create-role --role-name eks-demo-app-kubectl --assume-role-policy-document "$TRUST" --output text --query 'Role.Arn'
# COPIE O ARN GERADO POR ESTE ULTIMO COMANDO A CIMA.
