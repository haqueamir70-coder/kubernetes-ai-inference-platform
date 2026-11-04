# Implementation Plan

## Phase 0 — Architecture
Context and trust boundaries, workload profile, SLOs, threat model and ADRs. Exit: assumptions reviewed.

## Phase 1 — API and container
FastAPI contract, validation, health endpoints, tests, non-root image. Exit: CI tests and local smoke test pass.

## Phase 2 — Kubernetes baseline
Restricted namespace, probes, requests/limits, NetworkPolicy, Service and HPA. Exit: rendered manifests validate and local cluster rollout is verified.

## Phase 3 — Infrastructure
Terraform resource group, VNet and AKS subnet foundation. AKS/GPU compute remains an explicit opt-in cost decision. Exit: fmt/init/validate/plan reviewed and remote state secured.

## Phase 4 — Real inference
Optional vLLM adapter and GPU deployment profile. Exit: compatible GPU node, model licensing reviewed, API-to-runtime smoke test and load profile pass.

## Phase 5 — GitOps
Argo CD application and environment promotion. Exit: Git commit reconciles in non-production and rollback by Git revert is demonstrated.

## Phase 6 — Autoscaling
HPA for resource metrics; KEDA as an alternative when Prometheus exposes a real, validated workload metric. Exit: load test proves scale behavior without oscillation or overload.

## Phase 7 — Progressive delivery
Argo Rollouts canary profile. Exit: traffic routing and metric-based AnalysisTemplate are installed and a bad release is automatically aborted.

## Phase 8 — Security and observability
Trivy scan, SBOM/signing extension, Prometheus Operator and OpenTelemetry. Exit: real metrics endpoint, dashboards, alert rules and security findings are validated.

## Phase 9 — Operational readiness
SLOs, runbooks, ownership, game days, recovery and cost-per-1k-request reporting. Exit: incident exercise completed with actions assigned.

## Environment-specific gates
This repository is a reference implementation. It does not claim an AKS cluster, GPU node pool, Argo CD controller, KEDA operator, Prometheus Operator or OTel operator has been installed. Those require a target subscription/cluster, cost approval, credentials, and validation evidence.
