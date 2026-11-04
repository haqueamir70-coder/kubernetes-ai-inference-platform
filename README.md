# Kubernetes AI Inference Platform

<p align="center"><strong>A production-minded reference platform for deploying, scaling, securing, and observing AI inference workloads on Kubernetes.</strong></p>

<p align="center">
  <img alt="Kubernetes" src="https://img.shields.io/badge/Kubernetes-platform-326CE5?logo=kubernetes&logoColor=white">
  <img alt="Terraform" src="https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white">
  <img alt="GitOps" src="https://img.shields.io/badge/Delivery-GitOps-ef7b4d">
  <img alt="Security" src="https://img.shields.io/badge/Security-DevSecOps-0A7B62">
  <img alt="Observability" src="https://img.shields.io/badge/Observability-OpenTelemetry-5B5BD6?logo=opentelemetry&logoColor=white">
  <img alt="Status" src="https://img.shields.io/badge/Status-Reference%20Implementation-orange">
</p>

> **Status and honesty:** This repository contains a runnable API scaffold, Kubernetes deployment baseline, CI workflow, Terraform foundation, architecture documentation, and operational guidance. Cloud infrastructure, Argo CD, KEDA, GPU serving, canary automation, and production telemetry integrations are documented extension phases—not claimed as deployed or validated in a live production environment.

## Executive overview

Serving an AI model reliably is not simply deploying a container. A platform must make deliberate decisions about model lifecycle, request concurrency, accelerator scheduling, workload isolation, scaling signals, release safety, software supply chain, observability, cost, and incident response.

This project builds those platform-engineering capabilities incrementally. The first milestone is deliberately cloud-local and testable: a small inference API scaffold, hardened Kubernetes workload, Terraform starting point, and CI checks. Later milestones integrate GitOps, queue-aware autoscaling, progressive delivery, model-serving runtimes, and production observability.

## Reference architecture

![Kubernetes AI inference reference architecture](docs/architecture/platform-reference-architecture.svg)

### Request lifecycle

1. Client traffic enters through an ingress or API gateway with TLS and authentication.
2. Kubernetes routes requests to healthy inference API pods through a Service.
3. The API validates input and calls an inference adapter. The included adapter is deterministic scaffolding; it does not load a machine-learning model.
4. Workload, application, and infrastructure telemetry is exported without logging sensitive request payloads.
5. Scaling and rollout policies are introduced only after measurable workload signals and SLOs exist.

## Technology decisions

| Capability | Baseline | Extension / decision gate |
|---|---|---|
| Infrastructure | Terraform | Azure AKS, network, identity, remote state |
| Runtime | Kubernetes | GPU node pools only when model benchmarks justify them |
| Packaging | Kustomize | Helm when multi-tenant parameterization warrants it |
| Delivery | GitHub Actions CI | Argo CD GitOps reconciliation |
| Autoscaling | HPA-compatible resource metrics | KEDA when a real queue or external metric source exists |
| Releases | Kubernetes rolling update | Argo Rollouts canary after metrics-based analysis is defined |
| Security | Pod hardening, NetworkPolicy, image scan | Signing and admission verification |
| Telemetry | Health endpoints and structured logs | OpenTelemetry, Prometheus, Grafana, tracing backend |
| Model serving | Adapter interface | vLLM, Triton, or another runtime selected by model/latency/GPU constraints |

## Repository structure

```text
.
├── .github/workflows/          # CI checks
├── docs/
│   ├── architecture/           # SVG reference architecture
│   ├── decisions/              # Architecture decision records
│   ├── runbooks/               # Operational procedures
│   ├── scenarios/              # Senior-level design/incident exercises
│   └── implementation-plan.md  # Phased delivery plan
├── deploy/app/                 # Kubernetes base and local overlay
├── infra/terraform/            # Terraform foundation example
├── src/inference-api/          # Runnable API scaffold and tests
├── security/                   # Threat model and security baseline
└── scripts/                    # Local validation helper
```

## Run locally

Prerequisites: Docker, kubectl, and a local cluster such as kind or minikube. Python 3.12 is required only to run the API/tests without a container.

```bash
# Run API and tests without Docker
cd src/inference-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app:app --host 127.0.0.1 --port 8000

# Or build the container from repository root
docker build -t ai-inference-api:dev ./src/inference-api

# With kind: load the local image, then deploy
kind load docker-image ai-inference-api:dev
kubectl apply -k deploy/app/overlays/local
kubectl -n ai-inference rollout status deployment/inference-api
kubectl -n ai-inference port-forward svc/inference-api 8080:80
curl -fsS http://127.0.0.1:8080/healthz
curl -fsS -X POST http://127.0.0.1:8080/v1/infer \
  -H 'Content-Type: application/json' \
  -d '{"model":"demo-model","input":"platform engineering"}'
```

The example endpoint returns a deterministic demonstration response. It is not a model prediction. The default image name and local overlay assume the image has been loaded into the cluster.

## Phased delivery roadmap

| Phase | Deliverable | Exit evidence |
|---|---|---|
| 0 — Architecture | Context, trust boundaries, SLOs, ADRs, threat model | Reviewed design and explicit assumptions |
| 1 — API baseline | Input validation, health endpoints, tests, container | CI passes; local smoke test succeeds |
| 2 — Kubernetes baseline | Namespace, hardened deployment, Service, NetworkPolicy | Pods healthy; policies and security context reviewed |
| 3 — IaC foundation | Terraform resource-group/VNet/subnet starting point | fmt/validate/plan; remote-state design reviewed |
| 4 — GitOps | Argo CD app-of-apps or environment application | Git commit reconciles and drift is observable |
| 5 — Autoscaling | HPA baseline, then KEDA for real external metrics | Load-test evidence, scale behavior, capacity/cost model |
| 6 — Progressive delivery | Canary metrics and rollback policy | Failure injection aborts bad release |
| 7 — Security & telemetry | SBOM, scans, signing, OTel metrics/traces/logs | Security gates and useful dashboards |
| 8 — Operational readiness | SLOs, runbooks, game days, recovery | Evidence of rollback and incident exercise |

Detailed deliverables: [Implementation plan](docs/implementation-plan.md).

## Reliability and SLO design

Set objectives from measured workload baselines; example targets are not service commitments. Define:
- **Availability:** successful eligible inference requests divided by eligible requests.
- **Latency:** p50/p95/p99 end-to-end latency segmented by model and payload size.
- **Saturation:** queue depth, in-flight requests, CPU throttling, memory pressure, GPU utilization, and pending pods.
- **Correctness:** valid response/schema rate and model/runtime error rate.

Alert on sustained user impact and error-budget burn, not CPU utilization in isolation.

## Security baseline

- Run non-root, drop Linux capabilities, use RuntimeDefault seccomp, and read-only root filesystem where compatible.
- Define CPU/memory requests and limits; enforce namespace quotas.
- Use default-deny network policy and explicitly allow required traffic.
- Pin production images by immutable digest.
- Scan source, dependencies, IaC, and container images; retain an SBOM.
- Use workload identity and short-lived credentials; never store secrets in Git.
- Restrict RBAC and separate platform administration from application deployment.
- Do not log raw prompts, secrets, customer data, or model payloads by default.

See [threat model](security/threat-model.md).

## Operations

Runbooks: [API unavailable](docs/runbooks/api-unavailable.md) · [Latency and saturation](docs/runbooks/high-latency.md) · [Release rollback](docs/runbooks/rollback.md).

## Senior-level engineering scenarios

See [interview scenarios](docs/scenarios/senior-engineering-scenarios.md), covering GPU capacity, queue-based scaling, zero-downtime model rollout, Terraform state recovery, supply-chain compromise, and regional failure.

## Contribution and validation

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Run `scripts/validate.sh` for local repository checks. CI runs tests, YAML parsing, and Terraform formatting/validation where the Terraform binary is available.

## Roadmap

See [docs/implementation-plan.md](docs/implementation-plan.md). The project will mark features as implemented only when code, tests, and reproducible validation evidence are committed.
