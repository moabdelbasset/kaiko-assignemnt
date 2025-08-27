from fastapi.testclient import TestClient
from services.data_processor.app.main import app

def test_process():
    c = TestClient(app)
    payload = [{"id": "a", "values": [1,2,3]}, {"id": "b", "values": [10,10,10]}]
    r = c.post("/process", json=payload)
    assert r.status_code == 200
    js = r.json()
    assert len(js) == 2
    # mean/std sanity checks
    assert abs(js[0]["mean"] - 2.0) < 1e-6
    assert js[1]["std"] == 0.0
