# Runbook: GPU capacity and inference saturation

## Signals
Track GPU utilization and memory, model load time, queue depth, in-flight requests, token throughput, p95/p99 latency, pending GPU pods, and cost per successful request.

## Triage
1. Confirm the affected model/version and traffic cohort.
2. Inspect pod events and node allocatable GPU resources.
3. Inspect NVIDIA device plugin health and GPU telemetry.
4. Separate GPU compute saturation from VRAM pressure, CPU tokenization bottlenecks, and request queueing.
5. Check batch size, max model length, concurrency, and model cache hit rate.

## Mitigation
Apply admission control and bounded queueing first. Scale only when schedulable GPU capacity exists. Consider a smaller/quantized model or lower concurrency only after quality and latency tests. Do not silently fall back to CPU for GPU-bound workloads.

## Recovery
Run a representative load test; confirm p95/p99, throughput, error rate, GPU memory headroom, and cost/request. Record model/runtime/driver versions.
