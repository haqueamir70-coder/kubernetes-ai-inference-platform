# Runbook: Inference API unavailable

## Impact and signals
Clients see connection failures, 5xx responses, or readiness failures. Confirm impact before changing infrastructure.

## Triage
1. `kubectl -n ai-inference get deploy,pods,svc -o wide`
2. `kubectl -n ai-inference get events --sort-by=.lastTimestamp`
3. `kubectl -n ai-inference describe deployment inference-api`
4. `kubectl -n ai-inference logs deploy/inference-api --all-containers --tail=200`
5. `kubectl -n ai-inference get endpoints inference-api`

## Common causes
- **Image pull failure:** verify registry reachability, image digest/tag, and pull authorization.
- **CrashLoopBackOff:** inspect previous logs and startup configuration.
- **Readiness failure:** validate port/path and application initialization.
- **No endpoints:** verify Service selectors against pod labels.
- **Network failure:** inspect ingress, NetworkPolicy, DNS, and CNI enforcement.

## Mitigation
If a bad rollout caused the issue, use the rollback runbook. Restore replicas only after confirming node capacity and downstream health. Do not bypass authentication or network controls as a quick fix.

## Recovery verification
Confirm ready endpoints, synthetic request success, stable error rate/latency, and alert clearance. Record timeline, cause, mitigation, and prevention actions.
