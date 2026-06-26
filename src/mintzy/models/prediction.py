from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import pandas as pd

class PredictionRow(BaseModel):
    Ticker: str
    Date: str
    Time: str
    Predicted_Price: float

class PredictionResponse(BaseModel):
    success: bool
    data: List[PredictionRow]
    credits_remaining: int
    timestamp: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def to_dataframe(self) -> "pd.DataFrame":
        return pd.DataFrame([row.model_dump() for row in self.data])

class PredictionEvent(BaseModel):
    type: str
    status: Optional[str] = None
    message: Optional[str] = None
    ticker: Optional[str] = None
    predictions: Optional[List[PredictionRow]] = None
    warnings: Optional[List[str]] = None
    credits_remaining: Optional[int] = None
    tickers_processed: Optional[List[str]] = None
