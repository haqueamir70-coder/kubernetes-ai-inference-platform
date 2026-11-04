# Implementation Plan

## Delivery principles
1. Deliver small increments with reproducible evidence.
2. Add controllers and cloud services only for defined requirements.
3. Keep cloud spend opt-in; review Terraform plans before apply.
4. Mark capabilities complete only when code, tests, and validation evidence exist.
5. Never commit state files, credentials, kubeconfigs, model weights, or customer prompts.

## Phase 0 — Architecture and requirements
**Deliverables:** context, container, deployment and trust-boundary diagrams; workload profile (model format, schema, concurrency, payload size, throughput, latency, accelerator profile); SLO definitions; threat model; ADRs.
**Exit gate:** architecture review; assumptions and non-goals explicit.

## Phase 1 — API and container baseline
**Deliverables:** request validation, health endpoints, tests, non-root image, CI test job.
**Exit gate:** tests pass and local smoke test is reproducible. Current adapter is deterministic demo scaffolding, not an ML model.

## Phase 2 — Kubernetes workload baseline
**Deliverables:** namespace, service account, deployment, Service, NetworkPolicy, probes, resource requests/limits, restricted security context, local Kustomize overlay.
**Exit gate:** rendered manifests validate and local cluster rollout succeeds. NetworkPolicy must be tested with the selected CNI and actual gateway namespace labels.

## Phase 3 — Terraform foundation
**Deliverables:** resource group, VNet, AKS subnet example, environment tfvars, outputs, remote backend design.
**Exit gate:** fmt/init/validate/reviewed plan. This example does not create AKS or incur compute cost. Add cluster resources only after identity, networking, policy, and cost reviews.

## Phase 4 — GitOps
**Deliverables:** Argo CD installation, least-privilege project, environment Applications, immutable image promotion and drift detection.
**Exit gate:** reviewed Git change reconciles into non-production; rollback by Git revert demonstrated.

## Phase 5 — Scaling and performance
**Deliverables:** load profile, HPA baseline, KEDA only with real queue/external metrics, CPU/memory/GPU capacity model.
**Exit gate:** scale-out/in measured; no oscillation or overload cascade.

## Phase 6 — Progressive delivery
**Deliverables:** canary strategy, traffic split, analysis templates, metric-based abort, model compatibility/warm-up plan.
**Exit gate:** injected bad release aborts without violating agreed SLOs.

## Phase 7 — DevSecOps and observability
**Deliverables:** dependency/secret/IaC/image scans, SBOM, signing/provenance policy, OTel instrumentation, dashboards/alerts, payload redaction.
**Exit gate:** findings triaged; alerts actionable; telemetry overhead measured.

## Phase 8 — Operational readiness
**Deliverables:** ownership/on-call, SLO review, rollback/restore runbooks, game days, post-incident review, cost-per-1k-requests and GPU utilization view.
**Exit gate:** game day completed and actions assigned.
