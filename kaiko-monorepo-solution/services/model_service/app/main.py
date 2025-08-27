from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from common_utils import get_logger, setup_logging
import numpy as np
from sklearn.linear_model import LinearRegression

setup_logging()
log = get_logger("model-service")
app = FastAPI(title="Model Service", version="1.0.0")

class TrainRequest(BaseModel):
    X: list[list[float]]
    y: list[float]

class PredictRequest(BaseModel):
    X: list[list[float]]

_model = LinearRegression()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/train")
def train(req: TrainRequest):
    X = np.array(req.X, dtype=float)
    y = np.array(req.y, dtype=float)
    _model.fit(X, y)
    return {"coef": _model.coef_.tolist(), "intercept": float(_model.intercept_)}

@app.post("/predict")
def predict(req: PredictRequest):
    X = np.array(req.X, dtype=float)
    preds = _model.predict(X).tolist()
    return {"predictions": preds}

def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
