# Demo

## Prerequisites
- Kubernetes cluster
- kubectl
- Argo Workflows
- Argo Events with event bus

## Setup
Note: namespaces are hardcoded in the example files. You can change them if you want to use different namespaces.
- Add sensor and sensor rbac
```commandline
kubectl apply -f example/sensor-wf.yaml
kubectl apply -f example/sensor-rbac.yaml
```
- Add event source
```commandline
kubectl apply -f example/webhook.yaml
```
- Add workflow rbac
```commandline
kubectl apply -f example/workflow-rbac.yaml
```
- Add worker pod in default namespace
```commandline
kubectl apply -f example/worker.yaml
```

## How to run the demo
Bellow is an example of a webhook payload that can be sent to the Argo Events sensor. This payload simulates a scenario where a pod is using excessive CPU resources, which could indicate a potential crypto miner. You can use a tool like `curl` or Postman to send this payload to the webhook endpoint configured in the Argo Events sensor.

```json
{
  "receiver": "webhook",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "CryptoMinerDetected",
        "severity": "critical",
        "instance": "docker-desktop",
        "job": "kubernetes-nodes",
        "namespace": "default",
        "pod": "worker",
        "container": "ubuntu",
        "reason": "High_CPU_Usage",
        "threshold": "90"
      },
      "annotations": {
        "summary": "Potential crypto miner detected",
        "description": "Pod suspicious-pod in namespace default is using 95% CPU, exceeding the 90% threshold. This may indicate unauthorized crypto mining.",
        "recommended_action": "Investigate the pod and consider isolating it."
      },
      "startsAt": "2025-03-18T10:00:00Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "http://prometheus.local/graph?g0.expr=rate(container_cpu_usage_seconds_total[5m])>0.9",
      "fingerprint": "abc123"
    }
  ],
  "groupLabels": {
    "alertname": "CryptoMinerDetected"
  },
  "commonLabels": {
    "alertname": "CryptoMinerDetected",
    "severity": "critical"
  },
  "commonAnnotations": {
    "summary": "Potential crypto miner detected",
    "description": "Pod suspicious-pod-xyz in namespace default is using 95% CPU, exceeding the 90% threshold. This may indicate unauthorized crypto mining."
  },
  "externalURL": "http://alertmanager.local",
  "version": "4",
  "groupKey": "{}:{alertname=\"CryptoMinerDetected\"}"
}
```

#### curl example:
```commandline
curl -d '{"receiver":"webhook","status":"firing","alerts":[{"status":"firing","labels":{"alertname":"CryptoMinerDetected","severity":"critical","instance":"docker-desktop","job":"kubernetes-nodes","namespace":"default","pod":"worker","container":"ubuntu","reason":"High_CPU_Usage","threshold":"90"},"annotations":{"summary":"Potential crypto miner detected","description":"Pod suspicious-pod in namespace default is using 95% CPU, exceeding the 90% threshold. This may indicate unauthorized crypto mining.","recommended_action":"Investigate the pod and consider isolating it."},"startsAt":"2025-03-18T10:00:00Z","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://prometheus.local/graph?g0.expr=rate(container_cpu_usage_seconds_total[5m])>0.9","fingerprint":"abc123"}],"groupLabels":{"alertname":"CryptoMinerDetected"},"commonLabels":{"alertname":"CryptoMinerDetected","severity":"critical"},"commonAnnotations":{"summary":"Potential crypto miner detected","description":"Pod suspicious-pod-xyz in namespace default is using 95% CPU, exceeding the 90% threshold. This may indicate unauthorized crypto mining."},"externalURL":"http://alertmanager.local","version":"4","groupKey":"{}:{alertname=\"CryptoMinerDetected\"}"}' -H "Content-Type: application/json" -X POST http://localhost:12000/notify -H "Authorization: Bearer test"
```
