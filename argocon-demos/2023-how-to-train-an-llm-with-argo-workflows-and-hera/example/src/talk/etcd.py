"""The `etcd` module provides the ability to create, delete, and wait for etcd resources.

Note that there's a reference to a storage class name called `ssd`. See the `ssd` module for more details.
"""
from talk.workflows import Container, Parameter, Resource, m

# the etcd load balancer resource exposes the etcd replica set to the outside world and within the cluster. One could
# also experiment with using the ClusterIP service type
create_etcd_load_balancer = Resource(
    name="create-etcd-load-balancer",
    action="create",
    manifest="""
apiVersion: v1
kind: Service
metadata:
  name: etcd-client
spec:
  type: LoadBalancer
  ports:
    - name: etcd-client
      port: 2379
      protocol: TCP
      targetPort: 2379
  selector:
    app: etcd""",
    outputs=Parameter(
        name="etcd-svc-name", value_from=m.ValueFrom(json_path="metadata.name")
    ),
)

# the etcd stateful set provides 3 replicate of etcd
create_etcd_stateful_set = Resource(
    name="create-etcd-stateful-set",
    action="create",
    manifest="""
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: etcd
  labels:
    app: etcd
spec:
  serviceName: etcd
  selector:
    matchLabels:
      app: etcd
  replicas: 3
  template:
    metadata:
      name: etcd
      labels:
        app: etcd
    spec:
      containers:
        - name: etcd
          image: quay.io/coreos/etcd:latest
          ports:
            - containerPort: 2379
              name: client
            - containerPort: 2380
              name: peer
          volumeMounts:
            - name: data
              mountPath: /var/run/etcd
          command:
            - /bin/sh
            - -c
            - |
              PEERS="etcd-0=http://etcd-0.etcd:2380,etcd-1=http://etcd-1.etcd:2380,etcd-2=http://etcd-2.etcd:2380"
              exec etcd --name ${HOSTNAME} \
                --listen-peer-urls http://0.0.0.0:2380 \
                --listen-client-urls http://0.0.0.0:2379 \
                --advertise-client-urls http://${HOSTNAME}.etcd:2379 \
                --initial-advertise-peer-urls http://${HOSTNAME}:2380 \
                --initial-cluster-token etcd-cluster-1 \
                --initial-cluster ${PEERS} \
                --initial-cluster-state new \
                --data-dir /var/run/etcd/default.etcd
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        storageClassName: ssd
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi""",
)

# the delete resource removes the etcd client load balancer and the stateful set. Useful for cases when you want to
# dynamically spin up an etcd cluster and then delete it after the client application is done
delete_etcd_resources = Resource(
    name="delete-etcd-pod",
    action="delete",
    flags=["svc/etcd-client", "sts/etcd"],
)

"""Wait for the etcd load balancer to get an IP address.

This is a workaround for the fact that the etcd load balancer does not get an IP address immediately after it is
created. This script will wait until the load balancer has an IP address before exiting and expose the IP via an
output parameter.
"""
wait_for_etcd_ip = Container(
    name="wait-for-etcd-load-balancer-ip",
    image="alpine/k8s:1.23.17",
    command=["bash -c"],
    args=[
        'etcd_ip=""; while [ -z $etcd_ip ]; do echo "Waiting for end point..."; etcd_ip=$(kubectl get svc etcd-client --template="{{range .status.loadBalancer.ingress}}{{.ip}}{{end}}"); [ -z "$etcd_ip" ] && sleep 10; done; echo "End point ready-" && echo $etcd_ip > /etcd-ip;'
    ],
    inputs=Parameter(name="service-name"),
    outputs=Parameter(name="etcd-ip", value_from=m.ValueFrom(path="/etcd-ip")),
)
