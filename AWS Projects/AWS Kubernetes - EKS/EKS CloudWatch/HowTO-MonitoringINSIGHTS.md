# Tutorial para fazer monitoramento com o CloudWatch Metrics and Logs Groups utilizando EKS:

    # Anexe a política aos seus nós de processamentos: (NODES)
        1. Abra o console no EC2
        2. Selecione uma Ec2 e procure por security -> modify iam
        3. Vá em IAM, procure pela role que está anexada na instancia.
        4. Nesta role adicione "attach policy" e procure pela política < CloudWatchAgentServerPolicy >
        5. Anexe!

# Crie um IAM ServiceAccount com a Política CloudWatchAgentServerPolicy.
        eksctl create iamserviceaccount \
            --name cluster-cloudwatch \
            --namespace kube-system \
            --cluster <cluster-name> \
            --attach-policy-arn <arn-of-CloudWatchAgentServerPolicy> \
            --override-existing-serviceaccounts \
            --approve

# Utilize o [ANNOTATE] para mapear o cloudwatch com EKS
# entre <> Coloque a ROLE que o EKS utiliza!!!!! Procure a Role diretamente no EKS Clusters, procure pelo ARN e copie e coloque entre <>
        kubectl annotate serviceaccount -n kube-system cluster-cloudwatch eks.amazonaws.com/role-arn=<>

# Configurar  o agente do CloudWatch para coletar metrics do Clusters.
#
# Etapa 1
[Criar-um-namespace]
>>    kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cloudwatch-namespace.yaml
#
# Etapa 2
[Criar-uma-conta-de-servico-no-cluster]
>> kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cwagent/cwagent-serviceaccount.yaml
#
# Etapa 3
[Criar-um-Configmap-para-o-agente-CloudWatch]
>> curl -O https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cwagent/cwagent-configmap.yaml

# OBS: EDITE ESTE ARQUIVO, PROCURE POR <cluster_name>, troque pelo nome do EKS Cluster e apague as {[]}, deixe somente o nome e as aspas: "MeuCluster"
#
# Etapa 4
[Implantar-o-agent-do-CloudWatch-como-um-DaemonSet]
>> kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cwagent/cwagent-daemonset.yaml
#
# 4.1 - Download do YAML Daemonset
>> curl -O  https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cwagent/cwagent-daemonset.yaml
# OBS: Neste YAML baixado, remova as # na sessao port no arquivo (cwagent-daemonset.yaml)
>> kubectl apply -f cwagent-daemonset.yaml
#
# Visualize se tudo deu certo:
#
>> kubectl get pods -n kube-system
>> kubectl get pods -ALL
#
# TroubleShooting
#
>> kubectl describe pod pod-name -n kube-system
>> kubectl logs pod-name -n kube-system

