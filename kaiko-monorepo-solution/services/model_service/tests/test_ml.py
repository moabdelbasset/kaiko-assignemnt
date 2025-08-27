from fastapi.testclient import TestClient
from services.model_service.app.main import app

def test_train_predict():
    c = TestClient(app)
    train_payload = {"X": [[0],[1],[2]], "y": [0,1,2]}
    r = c.post("/train", json=train_payload)
    assert r.status_code == 200
    pred_payload = {"X": [[3],[4]]}
    r2 = c.post("/predict", json=pred_payload)
    js = r2.json()
    assert "predictions" in js
    assert len(js["predictions"]) == 2
