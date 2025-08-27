from pydantic import BaseModel, Field
from typing import List, Any, Optional

class RecordIn(BaseModel):
    id: str = Field(..., description="Record identifier")
    values: list[float] = Field(..., description="Numeric values")

class RecordOut(BaseModel):
    id: str
    mean: float
    std: float
    meta: Optional[dict[str, Any]] = None
