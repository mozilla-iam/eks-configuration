#!/usr/bin/env python

import boto3
import argparse
import tempfile
from subprocess import call


parser = argparse.ArgumentParser(description='Perform a deployment to available Kubernetes clusters.')
parser.add_argument('--env', default='development', choices=['development', 'production'],
                    help='sets a target cluster environment (default: development)')
args = parser.parse_args()

kubeconfig_template = '''
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {}
    server: {}
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    namespace: default
    user: aws
  name: aws
current-context: aws
kind: Config
preferences: {{}}
users:
- name: aws
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - token
      - -i
      - {}
      command: heptio-authenticator-aws
'''


def build_kubeconfig(ca_data, endpoint, cluster):
    tf = tempfile.NamedTemporaryFile()
    tf.write(kubeconfig_template.format(ca_data, endpoint, cluster))

    # Further research required:
    # The kubectl subprocess call will fail without this
    tf.seek(0)

    return tf


def deploy_to_cluster(kubeconfig):
    app_path = "./kubernetes/app/" + args.env + "/"
    call(["kubectl", "--kubeconfig", kubeconfig, "apply", "-f", app_path])


client = boto3.client('eks', region_name='us-west-2')

for cluster in client.list_clusters()['clusters']:
    if "-" + args.env + "-" in cluster:
        endpoint = client.describe_cluster(name=cluster)['cluster']['endpoint']
        ca_data = client.describe_cluster(name=cluster)['cluster']['certificateAuthority']['data']
        tf = build_kubeconfig(ca_data, endpoint, cluster)
        deploy_to_cluster(tf.name)
