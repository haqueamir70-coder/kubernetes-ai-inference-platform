# Runbook: Roll back an unsafe release

## Preconditions
Identify last known-good immutable image digest and configuration revision. Confirm API/model artifact compatibility.

## Kubernetes rollback
```bash
kubectl -n ai-inference rollout history deployment/inference-api
kubectl -n ai-inference rollout undo deployment/inference-api
kubectl -n ai-inference rollout status deployment/inference-api
```

For GitOps environments, revert the offending Git commit or promote the known-good digest through the approved workflow. Avoid manual drift that GitOps will overwrite.

## Verify
- Ready replicas and endpoints restored.
- Synthetic inference request succeeds.
- Error rate and p95/p99 return to baseline.
- Model version/schema compatibility confirmed.
- No data migration or queue compatibility issue remains.

## Follow-up
Preserve logs and deployment metadata, open an incident review, identify missed gates, and add a regression test or rollout analysis check.
