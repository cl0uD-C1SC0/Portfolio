# **1 - Criar um provedor de identidade OIDC do IAM para o Cluster**

# **Observações**
# **Verifique se não há nenhum OIDC criado já:**

__aws eks describe-cluster --name <cluster-name> --query "cluster.identity.oidc.issuer" --output text__

# Listar todos os provedores OIDC do IAM na sua conta. Substitua <EXAMPLED539D4633E53DE1B716D3041E> (incluindo <>) pelo valor retornado pelo comando anterior.

__aws iam list-open-id-connect-providers | grep <EXAMPLED539D4633E53DE1B716D3041E>__

__----------------------------------------------------------------------------------------------------__
# CRIAR UM PROVEDOR DE IDENTIDADE OIDC DO IAM VIA CLI

__**eksctl utils associate-iam-oidc-provider --cluister <cluster-name> --approve**__

**----------------------------------------------------------------------------------------------------**
# CRIAR UM PROVEDOR DE IDENTIDADE OIDC DO IAM VIA CONSOLE
#    2- Selecione o nome do cluster e selecione a guia Configuration (Configuracao) 
#    3- No Detalhes Observe o valor do URL do provedor OpenID Connect
#    4- Abra o console do IAM
#    5- 5- No painel de navegacao, escolha Identiy Providers (Provedores de identidade). Se um fornecedor listado corresponder a URL do cluster, entao você já tem um provedor para o cluster. Se um provedor não estiver listado que corresponda à URL do seu cluster, você deverá criar um.
#    6- Para criar um provedor, selecione Adicionar Provedor
#    7- Para Provider Type (Tipo de provedor), escolha OpenID Connect
#    8- Em Provider URL (URL do provedor), cole o URL emissor OIDC do cluster e selecione Get thumbprint.
#    9- Para Audience (Público), insira sts.amazonaws.com e escolha Add provider (Adicionar Provedor.)

__----------------------------------------------------------------------------------------------------__

# **2 Faça o download de uma política do AWS Load Balancer Controller que permita que ele faça chamadas para APIs da AWS em seu nome.**

**curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.2.0/docs/install/iam_policy.json**

# **2.1 Crie uma política do IAM usando a política obtida por download.**

**aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json**

# **2.3 Crie um Service Account**

**eksctl create iamserviceaccount --cluster=eks-cluster --namespace=kube-system --name=aws-load-balancer-controller --attach-policy-arn=arn:aws:iam::<account-number>:policy/AWSLoadBalancerControllerIAMPolicy --override-existing-serviceaccounts --approve**

# **2.4 Instale o AWS Load Balancer Controller usando o Helm**

**kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=master"**

**helm repo add eks https://aws.github.io/eks-charts**

**helm repo update**

**helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller --set clusterName=<cluster-name> --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller -n kube-system**

# verifique:

> kubectl get deployment -n kube-system aws-load-balancer-controller

__----------------------------------------------------------------------------------------------------__
# PRESTE ATENÇÃO -> COLOQUE ESTES VALORES NAS SUBNETS PARA O AWS LOAD BALANCER CONTROLER + ALB INGRESS MAPEAR AS MESMAS.
__----------------------------------------------------------------------------------------------------__

# Vá para as subnets escolhidas para o ALB mapear e adicione as tags:

*Chave* **kubernetes.io/cluster/<cluster-name>**
*Valor* **shared**


# PARA SUBNETES PRIVADAS:
*Chave* **kubernetes.io/role/internal-elb**
*Valor* **1**

# PARA SUBNETS  PUBLICAS:
*Chave* **kubernetes.io/role/elb**
*Valor* **1**

# Agora só implementar um
# kind: Namespace
# kind: Deployment
# kind: Service (type: NodePort)
# kind: Ingress (Utilize os annotations abaixo) (ingress.yaml)

annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip

# Arquivo de exemplo completo: (full.yaml)
#
# UPDATE KUBECONFIG

aws eks --region <region-code> update-kubeconfig --name <cluster-name>


