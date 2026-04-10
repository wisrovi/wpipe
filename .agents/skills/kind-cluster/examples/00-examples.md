# Kind Cluster Examples

## Example 1: kind-config.yaml

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

## Example 2: GPU Test Pod

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

## Example 3: Commands Output

```bash
# Create cluster
$ kind create cluster --config=kind-config.yaml

# Verify nodes
$ kubectl get nodes --show-labels

NAME                 STATUS   ROLES           LABELS
gpu-cluster-control   Ready    control-plane   node-role.kubernetes.io/control-plane
gpu-cluster-worker1   Ready    <none>          resource=GPU,worker=worker1
gpu-cluster-worker2   Ready    <none>          resource=GPU,worker=worker2
gpu-cluster-worker3   Ready    <none>          resource=GPU,worker=worker3
gpu-cluster-worker4   Ready    <none>          resource=CPU,worker=worker4
gpu-cluster-worker5   Ready    <none>          resource=CPU,worker=worker5

# Deploy GPU test pod
$ kubectl apply -f test-worker1.yaml

# Check pod status
$ kubectl get pods -o wide

NAME                READY   STATUS      RESTARTS   AGE   NODE
gpu-test-worker1    0/1     Completed   0          5s    gpu-cluster-worker1

# View GPU info
$ kubectl logs gpu-test-worker1

+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.85.05    Driver Version: 525.85.05    CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla T4         Off     | 00000000:00:1E.0 Off |                    0 |
|                             0W /  70W |      0MiB / 15360MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

## Example 4: Results Table

```markdown
| worker_name | labels | available_gpu | result_by_pod | notes |
|-------------|--------|---------------|---------------|-------|
| worker1 | worker=worker1, resource=GPU | Yes | Success | Tesla T4 detected |
| worker2 | worker=worker2, resource=GPU | Yes | Success | Tesla T4 detected |
| worker3 | worker=worker3, resource=GPU | Yes | Success | Tesla T4 detected |
| worker4 | worker=worker4, resource=CPU | N/A | Success | CPU only |
| worker5 | worker=worker5, resource=CPU | N/A | Success | CPU only |
```
