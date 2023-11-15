"""The ssd module contains the definition of the custom ssd K8s storage class that's required for the talk."""

from talk.workflows import Resource

"""`create_ssd_storage_class` defines the K8s storage class required for an ssd that's created dynamically. 

K8s will create the necessary PersistentVolumeClaim and PersistentVolume resources when a pod requests a volume
rather than when the PVC/PV are _defined_. This helps avoid the risk of pod + volume zone mismatches. Note that this 
was tested in GCP / GKE specifically. If you have a different cloud provider you have to change the `provisioner` 
field.
"""
create_ssd_storage_class = Resource(
    name="create-ssd-storage-class",
    action="create",
    manifest="""
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: ssd
provisioner: kubernetes.io/gce-pd
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: pd-ssd
""",
)
