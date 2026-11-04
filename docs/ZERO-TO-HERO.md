# Zero-to-Hero Project Guide — Kubernetes AI Inference Platform

## 1. Business scenario
A product team wants to expose a large language model through an API. A single VM or laptop cannot safely serve concurrent requests with predictable latency, GPU utilization, authentication, scaling and rollout controls. The platform packages inference as a Kubernetes workload.

## 2. Target outcome
Provide an authenticated FastAPI gateway, vLLM model server, GPU-aware scheduling, resource controls, autoscaling, metrics, secure model/image provenance and GitOps delivery. GPU cluster deployment must be evidenced separately.

## 3. Request lifecycle
Client → API authentication/rate limit → request validation → vLLM queue/batching → GPU inference → response streaming → metrics/logs. Kubernetes schedules model pods onto GPU nodes; GitOps manages desired state and Terraform can provision AKS foundation.

## 4. Tool-by-tool
| Tool | Purpose | Why it matters |
|---|---|---|
| Python / FastAPI | HTTP inference gateway | Validation, auth, rate limits, API contracts |
| vLLM | LLM inference engine | Continuous batching and efficient KV-cache management |
| Docker | Package API/model runtime | Reproducible immutable image |
| Kubernetes | Orchestration | Scheduling, service discovery, rollout and recovery |
| GPU node pool / NVIDIA device plugin | Expose GPU resources | Pods request accelerator resources; drivers/runtime must match |
| HPA | Autoscale from metrics | CPU/memory/custom metrics; not GPU magic by itself |
| KEDA (optional) | Event-driven scaling | Queue/metric triggers; scaling policy must consider cold start |
| Prometheus / Grafana | Observability | TTFT, tokens/sec, queue depth, GPU memory and saturation |
| Terraform / AzureRM | AKS infrastructure | Reproducible cluster/network foundation |
| Argo CD / GitOps | Desired-state deployment | Auditable reconciliation and drift correction |
| Trivy / SBOM/signing (where configured) | Image security/provenance | Pin and verify exact artifact |
| Key Vault / Workload Identity | Secret and cloud identity | Avoid static credentials in manifests |

## 5. Delivery workflow
Build/test API → build container → scan dependencies and image → generate SBOM → publish immutable digest → update GitOps manifest → reconcile into cluster → validate GPU scheduling/model load → load test → tune concurrency and scaling.

## 6. Commands
```bash
docker build -t inference-api:dev .
docker run --rm -p 8000:8000 inference-api:dev
kubectl get nodes -o wide
kubectl describe node <gpu-node>
kubectl get pods -n inference
kubectl logs deploy/inference-api -n inference
kubectl top pods -n inference
```
GPU-specific checks require a real GPU node and installed driver/device plugin.

## 7. Scenario-based Q&A
**Q1. API latency suddenly increases. What do you inspect?**  
A: Separate gateway latency from model time. Inspect request queue, time-to-first-token, tokens/sec, batch size, concurrency, GPU utilization/VRAM, CPU throttling, network and model load events. Compare p50/p95/p99.

**Q2. Pods are Pending despite a healthy cluster.**  
A: Check node selectors/affinity, taints/tolerations, GPU resource requests, available GPU capacity, quota, PVC and image pull. A GPU workload cannot schedule on a CPU-only pool.

**Q3. GPU memory runs out.**  
A: Check model weight size/precision, max context length, KV cache, batch/concurrency, parallelism and other processes. Reduce concurrency/context or choose suitable GPU/quantization after quality testing.

**Q4. Why is HPA alone insufficient for LLM autoscaling?**  
A: CPU utilization may not correlate with inference queue or GPU saturation. Use custom metrics such as queue depth, request rate, active sequences and GPU metrics; account for model cold-start time.

**Q5. How do you secure model delivery?**  
A: Pin image and model artifact digests, scan dependencies, generate SBOM/provenance, verify signatures, restrict registry access, use workload identity for secrets, and limit direct access to the model server.

## 8. Troubleshooting
Model load failure: check artifact path, permissions, VRAM and model compatibility. Slow first token: cold start, model load, queueing or prompt length. OOM: KV cache/concurrency/context. No GPU visible: driver, device plugin, node labels and allocatable resources. Rollout unavailable: readiness probe and capacity.

## 9. Security, reliability and cost
Authenticate and rate-limit clients; isolate tenants; enforce request/token quotas; avoid public model-server exposure; set pod limits; use disruption-aware rollout; track cost per 1K tokens and GPU utilization; scale down only with cold-start SLOs considered.

## 10. Learning path
Python API → Docker → Kubernetes deployments/services/probes → GPU scheduling → LLM memory/throughput basics → vLLM → Prometheus metrics → autoscaling → GitOps → supply-chain security → AKS GPU lab.

## 11. Scope honesty
FastAPI/vLLM and Kubernetes patterns are documented in the project. AKS/GPU/operator behavior is not proven until a real GPU cluster has been deployed and load-tested.
