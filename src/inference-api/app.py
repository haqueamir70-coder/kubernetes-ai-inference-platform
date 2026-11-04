from __future__ import annotations

import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
START_TIME = time.time()

app = FastAPI(
    title="AI Inference API Scaffold",
    version=APP_VERSION,
    description="Deterministic API scaffold. Replace the adapter with a selected model runtime.",
)


class InferenceRequest(BaseModel):
    model: str = Field(min_length=1, max_length=128)
    input: str = Field(min_length=1, max_length=8192)


class InferenceResponse(BaseModel):
    model: str
    output: str
    mode: str = "demo"


class DemoInferenceAdapter:
    """Deterministic placeholder; deliberately does not claim to run an ML model."""

    def infer(self, model: str, text: str) -> str:
        return f"[demo:{model}] Received {len(text)} characters."


adapter = DemoInferenceAdapter()


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    # Replace with dependency/model readiness checks when a real runtime is integrated.
    return {"status": "ready"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION}


@app.post("/v1/infer", response_model=InferenceResponse)
def infer(request: InferenceRequest) -> InferenceResponse:
    try:
        output = adapter.infer(request.model, request.input)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Inference failed") from exc
    return InferenceResponse(model=request.model, output=output)


@app.get("/metrics-note")
def metrics_note() -> dict[str, str | float]:
    return {
        "status": "metrics integration pending",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "note": "Integrate a Prometheus/OpenTelemetry exporter before production use.",
    }
