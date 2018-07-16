# Monitoring in Kubernetes (WIP)

This folder contains Kubernetes resources for deploying a cluster and applications monitoring solution.
It uses the [Prometheus Operator](https://coreos.com/operators/prometheus/docs/latest/) by CoreOS for deploying managed Prometheus instances and AlertManagers. 
## Getting Started

Each component is defined in its own file, alphabetically sorted to match dependencies between them. For example 00-namespace.yml will create a namespace in your cluster called "monitoring" where other components are going to live in. 

### Prerequisites

kubectl must be correctly setup to talk to your cluster and you will need priviledges for creating a ClusterRole, ClusterRoleBinding, a Namespace and resources in it.

### Deploying 

In order to deploy a Prometheus instance ready to monitor your applications you have to:

```
kubectl apply -f 00-namespace.yml -f 10-prometheus-operator.yml
sleep 3
kubectl apply -f 15-prometheus-object.yml
```

If everything went good, you should be able to see a prometheus and a prometheus-operator pod in the monitoring namespace:

```
kubectl get pods --namespace=monitoring
NAME                                   READY     STATUS        RESTARTS   AGE
prometheus-operator-78cc99d846-k2jcx   1/1       Running       0          1m
prometheus-prometheus-0                3/3       Running       1          46s

```


### Monitoring my application

In order to make Prometheus scrape the metrics of your application, you need to have a Service resource defining your Pods. After that you have to create a ServiceMonitor object which will be discovered by Prometheus.
You can find a complete example of an application containing a Deployment, Service and ServiceMonitor objects in 40-example-app.yml

