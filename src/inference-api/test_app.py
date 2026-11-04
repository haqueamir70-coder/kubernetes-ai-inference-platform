from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_endpoint():
    assert client.get("/readyz").status_code == 200


def test_demo_inference_response():
    response = client.post("/v1/infer", json={"model": "demo-model", "input": "hello platform"})
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "demo-model"
    assert body["mode"] in {"demo", "vllm"}
    if body["mode"] == "demo":
        assert "14 characters" in body["output"]


def test_input_validation():
    assert client.post("/v1/infer", json={"model": "", "input": "x"}).status_code == 422


def test_request_limits():
    assert client.post("/v1/infer", json={"model": "demo", "input": "x", "max_tokens": 99999}).status_code == 422


def test_prometheus_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
