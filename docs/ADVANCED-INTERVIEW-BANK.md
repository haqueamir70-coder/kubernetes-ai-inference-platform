# Kubernetes AI Inference Platform — Advanced Interview Question Bank

> 40 additional questions and answers. Use with [ZERO-TO-HERO.md](./ZERO-TO-HERO.md). Validate all claims against source, CI and actual AKS/GPU evidence.

## Project context
- **Architecture:** Client → FastAPI authentication/rate limiting → vLLM inference queue/batching → GPU-backed model server → metrics and response; GitOps manages Kubernetes desired state.
- **Tools:** Python, FastAPI, vLLM, Docker, Kubernetes, GPU node pool/device plugin, HPA/KEDA, Prometheus/Grafana, Terraform, Argo CD, Trivy/SBOM where configured.
- **Failure modes:** TTFT spikes, VRAM OOM, GPU pods Pending, model cold starts, autoscaling that ignores queue depth.
- **Mitigation:** Measure TTFT/tokens/sec/queue/VRAM, size weights plus KV cache, inspect GPU allocatable resources and taints, scale using meaningful custom metrics.

## 40 questions with answers

### 1. What business problem does this platform solve?
It provides a controlled and scalable API for model inference rather than running ad hoc model processes on developer machines. It standardizes authentication, scheduling, observability and delivery.

### 2. Explain the end-to-end request flow.
A client calls FastAPI, the gateway authenticates and validates the request, then forwards it to vLLM. vLLM schedules sequences and executes inference on GPU resources; response and telemetry return through the service.

### 3. Why separate FastAPI and vLLM?
FastAPI handles API contracts, auth, quotas and application-specific validation; vLLM specializes in model serving, batching and GPU execution. Separation allows independent scaling and security boundaries.

### 4. What is vLLM?
An LLM serving engine designed for efficient inference throughput and memory management, including PagedAttention and continuous batching.

### 5. What is continuous batching?
New requests can join ongoing batches as sequences finish, improving GPU utilization compared with waiting for fixed batches to complete.

### 6. What is KV cache?
It stores attention key/value tensors for prior tokens so the model does not recompute them for every generated token. Memory use increases with context length and concurrent sequences.

### 7. What is time-to-first-token?
TTFT measures time from request acceptance until the first generated token. It is distinct from total response latency and tokens-per-second.

### 8. How do you size GPU memory?
Account for model weights, KV cache, activations, runtime overhead and fragmentation. Precision, context length, batch size and concurrency affect VRAM demand.

### 9. Why use GPU node pools?
They provide accelerator-capable VM capacity separate from general CPU workloads. Scheduling must match GPU resource requests, node labels, taints and driver/runtime compatibility.

### 10. What does the NVIDIA device plugin do?
It advertises available GPU resources to Kubernetes so pods can request accelerator capacity. It does not install a compatible driver or guarantee the model fits in memory.

### 11. Why is a pod Pending?
Check node selectors/affinity, taints/tolerations, GPU resource requests, allocatable capacity, quotas, PVC binding and image pull events. A GPU workload cannot schedule on a CPU-only node pool.

### 12. What causes CUDA out-of-memory?
Model weights plus KV cache and runtime allocations exceed available VRAM. Reduce context/concurrency/batch, select quantization or a larger GPU after measuring quality and performance.

### 13. What is the difference between HPA and KEDA?
HPA scales from resource or custom metrics; KEDA adds event/external-metric scalers and may support scale-to-zero patterns. Neither automatically understands LLM queue pressure unless suitable metrics are exposed.

### 14. Why can CPU-based HPA be ineffective?
Inference saturation is often GPU memory, queue depth or active sequence limited. CPU utilization may not correlate with user latency or GPU saturation.

### 15. Which metrics matter?
TTFT, inter-token latency, tokens/sec, request rate, queue depth, p50/p95/p99 latency, GPU utilization/VRAM, OOM count, model load time and error rate.

### 16. How do you troubleshoot rising latency?
Separate gateway and model time; inspect queue depth, prompt length, batch/concurrency, GPU saturation/VRAM, CPU throttling, model load events and network dependency latency.

### 17. What is a cold start?
The delay while a pod starts, downloads/loads model weights and warms runtime/GPU memory. Large model artifacts can dominate startup time.

### 18. How reduce cold-start impact?
Pre-pull images, stage model artifacts close to nodes, keep warm capacity for critical services, use readiness gates and plan rollout capacity. Balance warm replicas against GPU cost.

### 19. How protect the inference API?
Authenticate clients, enforce per-tenant quotas/rate limits, validate payload/token limits, cap concurrency and prevent direct public access to the model server.

### 20. How avoid one tenant exhausting GPUs?
Use quotas, concurrency limits, fair scheduling/queues, request size limits and tenant-level usage metrics. Define priority policy and load shedding.

### 21. How do Kubernetes readiness and liveness probes differ?
Readiness controls whether a pod receives traffic; liveness restarts a stuck process. Startup probes protect slow initialization before liveness/readiness checks begin.

### 22. How do you deploy a new model safely?
Pin model and container digests, stage capacity, load the model, verify readiness, route a small canary share, compare latency/error/quality signals and roll back on regression.

### 23. What happens during a rolling update?
Kubernetes gradually replaces pods according to deployment strategy and availability constraints. Model downloads and GPU capacity can make default rollout behavior unsuitable without planning.

### 24. Why use image digests?
Tags can be changed; a digest identifies exact image bytes. It ensures the scanned, signed and deployed artifact is the same content.

### 25. How manage model artifacts?
Use controlled object storage or model registry, immutable/versioned artifacts, checksums, access policies and provenance. Avoid pulling arbitrary model files at runtime.

### 26. How secure runtime secrets?
Use workload identity and a secret manager integration; avoid credentials in Docker layers, manifests, source code or logs. Restrict service-account permissions.

### 27. What role does GitOps play?
Git stores desired Kubernetes configuration; a controller reconciles the cluster to that state and reports drift. Rollback can be performed by reverting to a known-good commit/digest.

### 28. What is the role of Terraform?
It can provision cluster/network/identity foundation. Terraform does not replace Kubernetes manifests or the GitOps controller that manages in-cluster workloads.

### 29. How do you secure the container image?
Use minimal base images, non-root execution, vulnerability/dependency scans, SBOM, signature/provenance, immutable digest pinning and controlled registry access.

### 30. What is an SBOM?
A machine-readable inventory of software components and versions. It supports vulnerability analysis but does not itself prove an image is secure.

### 31. What is the difference between GPU utilization and throughput?
GPU utilization shows device activity; throughput measures useful output such as tokens/sec or requests/sec. High utilization can coexist with poor latency or inefficient batching.

### 32. How do you capacity plan?
Benchmark representative prompt/output lengths and concurrency, measure VRAM and tokens/sec, include headroom for rollout/failures and estimate GPU cost per 1K tokens.

### 33. How do you handle model-server failure?
Readiness removes unhealthy pods from service; Kubernetes restarts failed containers; multiple replicas and capacity-aware rollout improve availability. Verify model load and queue recovery after restart.

### 34. How do you design observability?
Expose request-level latency/error/throughput metrics, model-level TTFT/tokens/sec/queue metrics and infrastructure GPU/node metrics. Correlate traces/logs with request IDs while avoiding sensitive prompts.

### 35. What should not be logged?
Do not log API tokens, credentials or full sensitive prompts/responses by default. Use request IDs, sizes, timings and safe error categories with controlled retention.

### 36. What are the key cost drivers?
GPU instance hours, idle warm replicas, model storage/download, network egress, observability ingestion and overprovisioned CPU/memory. Track cost per token and utilization.

### 37. What does CI prove?
CI can prove code formatting, tests, image build and configured scans. It does not prove GPU scheduling, real model throughput, AKS networking or production availability.

### 38. What must be tested on real AKS/GPU?
Driver/device plugin compatibility, GPU scheduling, VRAM fit, model loading, load/latency, autoscaling, rollout, failure recovery, security and cost.

### 39. How would you explain a production incident to a CTO?
State user impact and duration, quantify latency/error changes, explain root cause and mitigation, show evidence, and list prevention actions with owners and dates.

### 40. What is implemented versus planned in this repository?
Inspect source, workflows and manifests. FastAPI/vLLM examples and Kubernetes patterns do not prove a live AKS/GPU deployment; report live cluster evidence separately.

## Source-code file-by-file deep dive

For every actual file, record its path and explain:
1. **Python/FastAPI:** imports, app entry point, routes, request/response models, validation, auth middleware, exception handling, async behavior, timeouts, logging, metrics and tests.
2. **vLLM config:** model identifier/revision, dtype/quantization, tensor parallelism, max model length, GPU memory utilization, batching/concurrency settings and compatibility assumptions.
3. **Dockerfile:** base image, build context, dependency installation, layers, non-root user, entrypoint, exposed port, health check and runtime filesystem.
4. **Kubernetes manifests:** Deployment, replicas, selectors, GPU resource requests, node selectors/taints, probes, limits, securityContext, service account, Service, HPA/KEDA and ingress.
5. **Terraform:** provider/backend, variables, VNet/subnets, AKS, node pools, identity, role assignments, outputs and state.
6. **GitHub Actions:** triggers, permissions, runner, setup, tests, image build/scan, registry auth, artifacts, deployment permissions and failure conditions.
7. **Prometheus/Grafana:** metric type/labels, scrape config, PromQL, dashboard panels, alert thresholds and runbooks.
8. **GitOps:** source repository, sync policy, health checks, image digest update, drift handling and rollback.

## Hands-on labs

- Build and run the API locally.
- Run a small model on supported hardware or a controlled hosted GPU environment.
- Inspect GPU resource visibility and pod scheduling on a disposable cluster.
- Load test with different context lengths and concurrency.
- Trigger an OOM or failed readiness in a test environment and diagnose it.
- Roll out a new digest and roll back to the previous one.
- Build an evidence matrix: implemented | CI-validated | cloud-deployed | planned.

## Scope rule
A GPU/AKS architecture diagram is not proof of a live GPU cluster. State exactly which code, workflow and runtime tests have been completed.
