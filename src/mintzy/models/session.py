from typing import Optional, Dict, Any
from pydantic import BaseModel

class AuthenticateResponse(BaseModel):
    session_id: str
    message: Optional[str] = None
    # VERIFY: assumed response shape

class VerifyTotpResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    # VERIFY: assumed response shape

class StartTradingResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    # VERIFY: assumed response shape

class StopTradingResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    # VERIFY: assumed response shape

class DashboardResponse(BaseModel):
    session_id: Optional[str] = None
    state: str
    positions: list[Dict[str, Any]] = []
    # VERIFY: assumed response shape
