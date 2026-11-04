# vLLM runtime profile

This optional profile deploys the official vLLM OpenAI-compatible server. It requires a Kubernetes node with a compatible NVIDIA GPU, NVIDIA device plugin/operator, sufficient VRAM, model registry access, and a model license review.

## Enable

1. Review the model and hardware sizing. Qwen2.5-1.5B-Instruct is the default example, not a capacity recommendation.
2. Build/load the API image and the vLLM image according to your registry policy.
3. Set `INFERENCE_BACKEND=vllm` on the API Deployment.
4. Apply `kubectl apply -k deploy/vllm`.
5. Verify `kubectl -n ai-inference rollout status deployment/vllm` and call the API smoke test.

Do not apply to a CPU-only local cluster. The Deployment requests one NVIDIA GPU and uses an ephemeral model cache; production should use a controlled artifact cache, immutable image digest, explicit model revision, and a persistent or pre-warmed model storage strategy.

The vLLM image tag is pinned to a release tag for reproducibility; production promotion should pin a verified digest.
