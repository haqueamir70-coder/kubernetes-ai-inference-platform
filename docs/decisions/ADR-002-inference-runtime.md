# ADR-002: Use an OpenAI-compatible vLLM runtime adapter

- **Status:** Accepted as an optional runtime integration
- **Date:** 2026-11-04

## Context
The platform API should be independent of a specific model-serving engine while supporting a practical self-hosted inference runtime.

## Decision
Add an opt-in adapter that calls the vLLM OpenAI-compatible chat completions endpoint. Keep deterministic demo mode as the default for CPU-only development. Provide a separate GPU-requesting Kubernetes profile.

## Consequences
- API contract remains stable across demo and vLLM backends.
- GPU scheduling, model licensing, artifact caching, and VRAM sizing remain environment-specific.
- The GPU profile must not be applied to a cluster without NVIDIA GPU support.
- Production requires authentication, TLS, request deadlines, observability, model revision pinning, and load testing.
