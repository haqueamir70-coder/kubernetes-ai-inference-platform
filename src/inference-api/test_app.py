from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_endpoint():
    response = client.get("/readyz")
    assert response.status_code == 200


def test_inference_demo_response():
    response = client.post(
        "/v1/infer",
        json={"model": "demo-model", "input": "hello platform"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "demo-model"
    assert body["mode"] == "demo"
    assert "14 characters" in body["output"]


def test_input_validation():
    response = client.post("/v1/infer", json={"model": "", "input": "x"})
    assert response.status_code == 422
