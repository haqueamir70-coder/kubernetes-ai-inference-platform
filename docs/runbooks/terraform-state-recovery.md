# Runbook: Terraform state lock and partial apply

## Stabilize
- Stop new applies and identify all pipelines/operators that may write state.
- Preserve the failed run logs and lock metadata.
- Confirm no Terraform process is still active.

## Inspect and back up
- Read the backend lock details and identify the lock owner.
- Pull a state backup to a secure, access-controlled location.
- Compare Terraform state with Azure resource inventory before changing either.

## Recover
- Use force-unlock only after proving the lock is stale and the owner is inactive.
- Run init and refresh-only plan where appropriate; inspect every proposed change.
- Import resources only after matching their real IDs and configuration.
- Never delete or hand-edit state as a first response.

## Verify
- Run a normal plan and explain every drift/change.
- Require peer review for production state operations.
- Record lock ID, operator, timestamps, backup location, root cause, and corrective action.
