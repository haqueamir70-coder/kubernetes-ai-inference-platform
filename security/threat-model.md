# Threat Model and Security Baseline

## Assets
- Model artifacts and integrity metadata.
- Inference inputs/outputs and customer data.
- Container images, source, build credentials, and deployment identities.
- Kubernetes API, cluster nodes, namespaces, and cloud control plane.
- Telemetry and operational records.

## Trust boundaries
1. External client to gateway/ingress.
2. Gateway to inference workload.
3. Workload to model artifact store and external dependencies.
4. CI system to artifact registry.
5. GitOps controller to Kubernetes API.
6. Platform administrators to tenant namespaces.

## Threats and mitigations

| Threat | Example | Mitigation |
|---|---|---|
| Unauthorized access | Public endpoint without auth | Gateway authentication, rate limits, network boundary |
| Prompt/data leakage | Request body copied into logs | Payload redaction; no raw prompt logging by default |
| Malicious image | Compromised dependency/base image | SBOM, scanning, immutable digest, signing/verification |
| Credential theft | Long-lived cloud key in pipeline | Workload identity/OIDC, short-lived tokens, secret manager |
| Container escape | Privileged pod or excess capabilities | Restricted security context, seccomp, non-root |
| Lateral movement | Unrestricted east-west traffic | Default-deny NetworkPolicy; validate actual CNI |
| Resource exhaustion | Huge payload or unbounded concurrency | Input limits, quotas, admission control, rate limiting |
| Model tampering | Mutable artifact URI | Versioned immutable artifacts and integrity verification |
| Pipeline abuse | Untrusted PR gets write token | Minimal permissions, isolated jobs, protected environments |

## Baseline controls
- Protect main and require review/status checks before production deployment.
- Use least-privilege GitHub Actions permissions.
- Never expose deployment credentials to untrusted pull requests.
- Use immutable image digests and approved registries in production.
- Scan images/dependencies and retain remediation evidence.
- Keep Kubernetes secrets, kubeconfigs, and Terraform state out of Git.
- Validate NetworkPolicy behavior with the selected CNI.
- Define data retention, access, and deletion rules for inference payloads.

## Residual risks
A scaffold cannot prove cloud identity posture, CNI enforcement, registry controls, GPU isolation, or compliance. These require environment-specific validation and review.
