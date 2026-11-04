#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/4] Python tests"
python -m pip install -r src/inference-api/requirements.txt
python -m pytest -q src/inference-api

echo "[2/4] Kubernetes manifests"
if command -v kubectl >/dev/null 2>&1; then
  kubectl kustomize deploy/app/overlays/local >/tmp/ai-inference-rendered.yaml
  echo "Kustomize render succeeded."
else
  echo "kubectl not installed; skipping manifest render."
fi

echo "[3/4] Terraform format and validation"
if command -v terraform >/dev/null 2>&1; then
  terraform fmt -check -recursive infra/terraform
  terraform -chdir=infra/terraform init -backend=false -input=false
  terraform -chdir=infra/terraform validate
else
  echo "terraform not installed; skipping Terraform checks."
fi

echo "[4/4] Done"
