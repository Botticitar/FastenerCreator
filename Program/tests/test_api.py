from fastapi.testclient import TestClient
from stepgen_app.main import app

client = TestClient(app)

def test_read_docs():
    """Verify the documentation endpoint is reachable."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_generate_screw_endpoint():
    """Verify that a valid screw request returns a file stream."""
    response = client.post("/v1/generate/screw", json={"diameter": 10, "length": 40})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/step"
    assert "attachment" in response.headers["content-disposition"]

def test_generate_washer_endpoint():
    """Verify that a valid washer request returns a file stream."""
    response = client.post("/v1/generate/washer", json={
        "inner_diameter": 13, 
        "outer_diameter": 24, 
        "thickness": 2
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/step"