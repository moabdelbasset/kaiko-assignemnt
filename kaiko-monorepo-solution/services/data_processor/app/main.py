from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd

from common_utils import get_logger, setup_logging, RecordIn, RecordOut

setup_logging()
log = get_logger("data-processor")
app = FastAPI(title="Data Processor", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process", response_model=List[RecordOut])
def process(records: List[RecordIn]):
    if not records:
        raise HTTPException(status_code=400, detail="No records provided")
    try:
        rows = [{"id": r.id, **{f"v{i}": v for i, v in enumerate(r.values)}} for r in records]
        df = pd.DataFrame(rows)
        value_cols = [c for c in df.columns if c.startswith("v")]
        stats = df[value_cols].agg(["mean", "std"], axis=1).rename(columns={"mean": "mean", "std": "std"})
        out = []
        for idx, r in enumerate(records):
            out.append(RecordOut(id=r.id, mean=float(stats.loc[idx, "mean"]), std=float(stats.loc[idx, "std"]), meta={"n": len(r.values)}))
        return out
    except Exception as e:
        log.exception("Processing failed")
        raise HTTPException(status_code=500, detail=str(e))

def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
