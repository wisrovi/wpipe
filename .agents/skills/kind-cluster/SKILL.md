---
name: kind-cluster
version: 1.0.0
description: "Crea cluster Kind con 1 control-plane y 5 workers (3 GPU, 2 CPU). Valida GPUs con pods nvidia-smi. USA cuando el usuario mencione 'crear cluster kind', 'kind cluster', 'kubernetes gpu', 'test gpu', 'nvidia-smi', o 'kind'."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [kubernetes, kind, gpu, docker, nvidia]
  requires: [kind, kubectl, docker, nvidia-docker]
inputs:
  - type: cluster_name
    description: Nombre del cluster (default: gpu-cluster)
outputs:
  - type: kubeconfig
    description: Cluster creado y funcional
  - type: validation_results
    description: worker_results.md con resultados de GPU
anti_trigger:
  - "Ya tengo el cluster"
triggers:
  - "crear cluster kind"
  - "kind cluster"
  - "kubernetes gpu"
  - "nvidia-smi"
  - "test gpu"
---

# Kind Cluster - GPU-Enabled Kubernetes Cluster

## Objetivo

Crear cluster Kind con:
- 1 control-plane
- 5 workers (3 GPU, 2 CPU)

---

## CONFIGURACIÓN

### kind-config.yaml

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: gpu-cluster
nodes:
- role: control-plane
- role: worker
  labels:
    worker: worker1
    resource: GPU
- role: worker
  labels:
    worker: worker2
    resource: GPU
- role: worker
  labels:
    worker: worker3
    resource: GPU
- role: worker
  labels:
    worker: worker4
    resource: CPU
- role: worker
  labels:
    worker: worker5
    resource: CPU
```

---

## VALIDACIÓN DE GPU

### NO USAR: `docker exec`

### USAR: Pod con nvidia-smi

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-test-worker1
spec:
  restartPolicy: Never
  nodeSelector:
    worker: worker1
  containers:
  - name: nvidia-smi
    image: nvidia/cuda:12.2.0-base-ubuntu22.04
    command: ["nvidia-smi"]
```

---

## COMANDOS

```bash
# Crear cluster
kind create cluster --config=kind-config.yaml

# Verificar nodos
kubectl get nodes --show-labels

# Validar GPU en cada worker
kubectl apply -f test-worker1.yaml
kubectl logs gpu-test-worker1
```

---

## worker_results.md

| worker_name | labels | available_gpu | result_by_pod | notes |
|-------------|--------|---------------|---------------|-------|
| worker1 | worker=worker1, resource=GPU | Yes/No | Success/Failed | - |
| worker2 | worker=worker2, resource=GPU | Yes/No | Success/Failed | - |
| worker3 | worker=worker3, resource=GPU | Yes/No | Success/Failed | - |
| worker4 | worker=worker4, resource=CPU | N/A | Success/Failed | CPU only |
| worker5 | worker=worker5, resource=CPU | N/A | Success/Failed | CPU only |
