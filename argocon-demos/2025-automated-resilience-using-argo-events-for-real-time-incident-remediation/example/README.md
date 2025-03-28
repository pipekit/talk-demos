

###
- Move to assets folder
```commandline
cd argocon-demos/2025-automated-resilience-using-argo-events-for-real-time-incident-remediation/assets
```

- install argo workflows
```commandline
ARGO_WORKFLOWS_VERSION="v3.6.5"
kubectl create namespace argo
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/${ARGO_WORKFLOWS_VERSION}/quick-start-minimal.yaml"
```

- install argo events
```commandline
kubectl create namespace argo-events
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install.yaml
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install-validating-webhook.yaml
kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/eventbus/native.yaml
```

- create webhook
```commandline
kubectl apply -n argo-events -f webhook.yaml
```

- apply sensor rbac
```commandline
kubectl apply -n argo-events -f sensor-rbac.yaml
```

- apply workflow rbac
```commandline
kubectl apply -n argo -f workflow-rbac.yaml
```

- apply sensor
```commandline
kubectl apply -n argo-events -f sensor-wf.yaml
```

- add worker pod in default namespace
```commandline
kubectl apply -f worker.yaml
```


curl -d '{"receiver":"webhook","status":"firing","alerts":[{"status":"firing","labels":{"alertname":"CryptoMinerDetected","severity":"critical","instance":"docker-desktop","job":"kubernetes-nodes","namespace":"default","pod":"worker","container":"ubuntu","reason":"High_CPU_Usage","threshold":"90"},"annotations":{"summary":"Potential crypto miner detected","description":"Pod suspicious-pod in namespace default is using 95% CPU, exceeding the 90% threshold. This may indicate unauthorized crypto mining.","recommended_action":"Investigate the pod and consider isolating it."},"startsAt":"2025-03-18T10:00:00Z","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://prometheus.local/graph?g0.expr=rate(container_cpu_usage_seconds_total[5m])>0.9","fingerprint":"abc123"}],"groupLabels":{"alertname":"CryptoMinerDetected"},"commonLabels":{"alertname":"CryptoMinerDetected","severity":"critical"},"commonAnnotations":{"summary":"Potential crypto miner detected","description":"Pod suspicious-pod-xyz in namespace default is using 95% CPU, exceeding the 90% threshold. This may indicate unauthorized crypto mining."},"externalURL":"http://alertmanager.local","version":"4","groupKey":"{}:{alertname=\"CryptoMinerDetected\"}"}' -H "Content-Type: application/json" -X POST http://localhost:12000/notify -H "Authorization: Bearer test"
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
