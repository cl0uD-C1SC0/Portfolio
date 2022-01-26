#!/bin/bash
echo ""
echo "Baixando o pacote"
echo ""
sudo wget https://dl.google.com/go/go1.16.4.linux-amd64.tar.gz /home/ec2-user
echo ""
echo "Extraindo o pacote"
echo ""
sudo tar -xf /home/ec2-user/go1.16.4.linux-amd64.tar.gz
echo ""
echo "Movendo o go/ para /usr/local"
echo ""
sleep 2
sudo mv /home/ec2-user/go /usr/local
echo ""
echo "Preparando o ambiente..."
echo `export GOROOT=/usr/local/go`
echo `export GOPATH=$HOME/Apps/app1`
echo `export PATH=$GOPATH/bin:$GOROOT/bin:$PATH`
echo ""
echo "Limpeza..."
sudo rm -rf /home/ec2-user/go1.16.4.linux-amd64.tar.gz
echo ""
echo "Verify Installation..."
echo ""
echo `go version`
echo ""
echo "Done!"

#