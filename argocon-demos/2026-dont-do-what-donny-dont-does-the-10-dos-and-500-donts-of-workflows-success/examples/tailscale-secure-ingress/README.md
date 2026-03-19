# Secure ingress to Argo Server using the Tailscale Kubernetes Operator

This example shows two ways to configure secure access to Argo Server using the Tailscale Kubernetes Operator:
- Standalone Ingress.
- HA Ingress (which uses a [ProxyGroup](https://tailscale.com/docs/features/kubernetes-operator/how-to/cluster-ingress#high-availability) for high availability and is most suitable for production use cases). 

##  Ingress over Tailscale

When an `Ingress` is exposed using the Tailscale Operator, it will not be accessible over the public internet by default. Instead, only authenticated users of the tailnet with correct permissions will have access (see [ACLs](https://tailscale.com/docs/features/access-control/acls)).

An `Ingress` is managed by the Tailscale Operator if it uses the `tailscale` ingress class (i.e. `spec.ingressClassName: tailscale`).

##  Pre-requisites

- A [Tailscale account](https://login.tailscale.com/start).
- A Kubernetes cluster with the [Tailscale Kubernetes operator installed](https://tailscale.com/docs/features/kubernetes-operator).
- [Enable HTTPS](https://tailscale.com/docs/how-to/set-up-https-certificates#configure-https) for your tailnet.

###  Configuring Ingress

1. Apply the `Ingress` or HA `Ingress` resource: `kubectl apply -f ingress.yaml` or `kubectl apply -f ha-ingress.yaml`.

2. The Operator will create the necessary resources in your cluster, and a [MagicDNS](https://tailscale.com/docs/features/magicdns) name and tls certificate will be provisioned for your `Ingress`. 

3. Wait for the ADDRESS field on your ingress to be populated with its [MagicDNS](https://tailscale.com/docs/features/magicdns) name:
```
kubectl get ing -n argo
NAME                    CLASS       HOSTS   ADDRESS                                  PORTS     AGE
argo-workflows-server   tailscale   *       argo-workflows-server.mytailnet.ts.net   80, 443   9s
```

4. To access the Argo Server UI using Tailscale, first ensure you are connected to your tailnet. Then, copy the MagicDNS name in the ADDRESS field (see example above) to access Argo Server in your browser.

You now have secure access to your Argo Workflows UI!

###  Next steps

- For more detail on securing Kubernetes ingress at L3 and L7, see https://tailscale.com/docs/features/kubernetes-operator/how-to/cluster-ingress.
- For more on use cases for securing connectivity within Kubernetes using Tailscale, see [Egress](https://tailscale.com/docs/features/kubernetes-operator/how-to/cluster-egress), [API-Server](https://tailscale.com/docs/features/kubernetes-operator/how-to/api-server-proxy) and [Multi-Cluster](https://tailscale.com/docs/features/kubernetes-operator/how-to/cross-cluster) documentation. 