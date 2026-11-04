# Runbook: High inference latency or saturation

## First response
1. Segment p95/p99 by model, version, request size, and route.
2. Check request rate, in-flight requests, queue depth, timeout rate, restarts, and pending pods.
3. Check CPU throttling, memory pressure/OOMs, GPU utilization and memory where applicable.
4. Check dependency latency and model load/warm-up time.

## Diagnosis
- Queue grows while replicas remain fixed: validate scaling signal, metric adapter, and KEDA/HPA configuration.
- CPU throttling is high: review CPU requests/limits and runtime concurrency.
- GPU memory is saturated: profile batch size, concurrency, model placement, and quantization.
- One model/version is slow: compare runtime and artifacts; isolate noisy neighbors if needed.
- Latency rises with downstream errors: investigate dependency saturation before adding replicas.

## Mitigation
Use admission control to protect the service, scale only within tested capacity, and route away from a degraded version when safe. Avoid retry amplification during overload.

## Closeout
Capture workload profile, before/after p95/p99, saturation signals, capacity change, and cost impact. Update SLO and autoscaling thresholds from evidence.
