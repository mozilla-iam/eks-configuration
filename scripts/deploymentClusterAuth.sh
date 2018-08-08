#!/usr/bin/env bash

# Update apt cache and install dependencies
apt update
apt install -y curl python-pip

pip install awscli --upgrade

curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/kubectl
curl -O https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/bin/linux/amd64/heptio-authenticator-aws

chmod +x kubectl
chmod +x heptio-authenticator-aws

# Move dependencies into path
mv heptio-authenticator-aws /usr/bin/heptio-authenticator-aws
mv kubectl /usr/bin/kubectl
