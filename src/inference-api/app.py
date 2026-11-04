from __future__ import annotations

import os
import time
import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

APP_VERSION = os.getenv("APP_VERSION", "0.2.0")
INFERENCE_BACKEND = os.getenv("INFERENCE_BACKEND", "demo").lower()
VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://vllm:8000/v1")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "not-needed")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
START_TIME = time.time()
HTTP_REQUESTS = Counter(
    "http_requests_total", "HTTP requests handled by the inference API",
    ["app", "route", "method", "status"],
)
HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds", "HTTP request duration in seconds",
    ["app", "route", "method"],
)

app = FastAPI(title="AI Inference Platform API", version=APP_VERSION)


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    route = request.url.path
    if route != "/metrics":
        HTTP_REQUESTS.labels("inference-api", route, request.method, str(response.status_code)).inc()
        HTTP_REQUEST_DURATION.labels("inference-api", route, request.method).observe(time.perf_counter() - started)
    return response


class InferenceRequest(BaseModel):
    model: str = Field(default=DEFAULT_MODEL, min_length=1, max_length=256)
    input: str = Field(min_length=1, max_length=8192)
    max_tokens: int = Field(default=256, ge=1, le=2048)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class InferenceResponse(BaseModel):
    model: str
    output: str
    mode: str


def run_inference(request: InferenceRequest) -> InferenceResponse:
    if INFERENCE_BACKEND == "demo":
        return InferenceResponse(
            model=request.model,
            output=f"[demo:{request.model}] Received {len(request.input)} characters.",
            mode="demo",
        )
    if INFERENCE_BACKEND != "vllm":
        raise HTTPException(status_code=503, detail="Unsupported inference backend")
    try:
        response = httpx.post(
            f"{VLLM_BASE_URL.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {VLLM_API_KEY}"},
            json={
                "model": request.model,
                "messages": [{"role": "user", "content": request.input}],
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
            },
            timeout=httpx.Timeout(90.0, connect=5.0),
        )
        response.raise_for_status()
        payload = response.json()
        output = payload["choices"][0]["message"]["content"]
        return InferenceResponse(model=request.model, output=output, mode="vllm")
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Inference runtime request failed") from exc


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready", "backend": INFERENCE_BACKEND}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION, "backend": INFERENCE_BACKEND}


@app.post("/v1/infer", response_model=InferenceResponse)
def infer(request: InferenceRequest) -> InferenceResponse:
    return run_inference(request)


@app.get("/metrics-note")
def metrics_note() -> dict[str, str | float]:
    return {
        "status": "Prometheus/OpenTelemetry exporter integration is a next step",
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }
