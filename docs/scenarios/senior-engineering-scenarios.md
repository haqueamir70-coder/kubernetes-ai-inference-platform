# Senior Engineering Interview Scenarios (8–12 Years)

Use these as architecture/incident discussions, not memorized scripts. Structure answers around business impact, assumptions, safe diagnosis, options/trade-offs, execution, rollback, and measurable verification.

## 1. GPU capacity and noisy-neighbor isolation
**Scenario:** One model team monopolizes GPU memory and causes tail-latency spikes for another.
**Discuss:** GPU node pools, taints/tolerations, device plugin, resource requests, MIG where supported, model-aware bin packing, quotas, priority, GPU telemetry, and cost per inference.
**Follow-up:** How do you distinguish compute saturation from memory pressure or a batching issue?

## 2. Queue depth rises but autoscaler does not scale
**Scenario:** Queue backlog and p99 latency breach the SLO while replicas remain fixed.
**Discuss:** scaling metric semantics, KEDA trigger/credentials, metric freshness, target values, max replicas, quotas, pending pods, node capacity, cooldown, and admission control.
**Follow-up:** When can scale-out make latency worse?

## 3. Zero-downtime model rollout
**Scenario:** A faster model has a different tokenizer and response contract.
**Discuss:** API/model versioning, shadow traffic, canary cohorts, warm-up, readiness, cache behavior, per-version metrics, compatibility window, immutable artifacts, and rollback.
**Follow-up:** Which signals automatically abort the canary?

## 4. Terraform state lock and partial apply
**Scenario:** A pipeline stops mid-apply and next run reports a lock; a production subnet appears partially changed.
**Discuss:** stop concurrent writers, inspect lock metadata and pipeline history, prove no active process remains, back up state, force-unlock only if stale, refresh, inspect plan, and use reviewed import/move operations if needed.
**Follow-up:** How do you reconcile cloud reality with Terraform state?

## 5. Container supply-chain compromise
**Scenario:** A critical dependency vulnerability is disclosed after deployment.
**Discuss:** SBOM/digest inventory, exploitability and exposure, promotion block, patched rebuild, signing/attestation, admission policy, credential rotation if compromise is indicated, and evidence preservation.
**Follow-up:** Why is rebuilding from a mutable tag insufficient?

## 6. Regional outage
**Scenario:** Primary region fails while inference is business critical.
**Discuss:** RTO/RPO, active-active versus warm standby, model artifact replication, registry/identity/secrets, DNS failover, data residency, reserved capacity, dependency topology, and game days.
**Follow-up:** What proves the secondary region is actually ready?

## 7. Retry storm and cascading failure
**Scenario:** Model registry slows down and several service layers retry aggressively.
**Discuss:** deadlines, bounded retries with jitter, retry budgets, circuit breakers, bulkheads, backpressure, admission control, graceful degradation, and idempotency.
**Follow-up:** Where should retries live to avoid retry multiplication?

## 8. Multi-tenant governance
**Scenario:** Teams share a cluster but use inconsistent security and resource settings.
**Discuss:** golden paths, namespace isolation, RBAC, quotas, policy-as-code, NetworkPolicy, workload identity, self-service templates, exception workflows, and auditability.
**Follow-up:** How do you measure platform adoption and developer experience?

## 9. Observability cost explosion
**Scenario:** Trace and log volume increases 10x after detailed instrumentation.
**Discuss:** cardinality, sampling, aggregation, retention tiers, redaction, prompt/body omission, label hygiene, team budgets, and cost per telemetry signal.
**Follow-up:** Which signals should not be sampled for reliable SLO calculations?

## 10. Burst traffic and model cold starts
**Scenario:** Demand spikes for 15 minutes, but loading the model takes several minutes.
**Discuss:** forecasting, warm pools/minimum replicas, predictive scaling limits, queueing, batching, admission control, autoscaler lag, reserved GPU capacity, and cost/performance trade-offs.
**Follow-up:** How do you prove latency objectives during a burst test?

## Answer framework
1. Clarify customer impact and SLO.
2. State assumptions and unknowns.
3. Give a safe diagnostic sequence.
4. Compare at least two options with trade-offs.
5. Include blast-radius limits and rollback.
6. Finish with measurable verification and prevention.
