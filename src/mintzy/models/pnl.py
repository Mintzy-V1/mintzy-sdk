from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class PnLRecord(BaseModel):
    date: str
    pnl: float
    # VERIFY: assumed response shape

class AggregatePnL(BaseModel):
    total_pnl: float
    records: List[PnLRecord] = []
    # VERIFY: assumed response shape

class LivePnL(BaseModel):
    session_id: str
    timestamp: datetime
    current_pnl: float
    # VERIFY: assumed response shape
