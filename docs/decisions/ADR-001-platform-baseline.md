# ADR-001: Establish a cloud-portable Kubernetes baseline

- **Status:** Accepted as initial reference direction
- **Date:** 2026-11-04

## Context
We need a demonstrable AI inference platform foundation without creating paid cloud resources or implying that a production cluster exists.

## Decision
Start with a deterministic API scaffold, hardened Kubernetes Deployment/Service, Kustomize overlays, a small Terraform network foundation example, and CI validation. Keep Argo CD, KEDA, progressive delivery, GPU serving, and telemetry backend integrations as separately gated extensions.

## Consequences
- Local validation is possible without a cloud subscription.
- The sample API is not an ML inference runtime.
- Terraform provisions network foundation resources only when intentionally applied.
- Later choices remain open until workload and SLO requirements are known.
