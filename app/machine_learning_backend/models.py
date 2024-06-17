from pydantic import BaseModel
from typing import List

# ========== Response Models (200 HTTP Code) ===========

class PredictImageDataResponseModel(BaseModel):
    fruit_class: int
    fruit_class_string: str
    cropped_img: str
    confidence: float,
    freshness_percentage: str
    freshness_days: int

class PredictImageResponseModel(BaseModel):
    orig_img: str
    inferences: List[PredictImageDataResponseModel]
