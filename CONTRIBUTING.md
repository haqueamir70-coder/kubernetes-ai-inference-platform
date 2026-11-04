# Contributing

## Workflow
1. Open an issue describing the concern and expected outcome.
2. Create a focused branch and keep changes small.
3. Add or update tests and documentation.
4. Run `scripts/validate.sh` locally.
5. Open a pull request with risk, validation evidence, and rollback notes.

## Standards
- Prefer immutable versions and explicit resource contracts.
- Never commit secrets, Terraform state, kubeconfigs, private model artifacts, or customer prompts.
- Keep examples safe to run locally; cloud provisioning must be opt-in.
- Mark integrations as planned until working configuration and validation evidence exist.
- Include operational impact and security implications in design changes.
