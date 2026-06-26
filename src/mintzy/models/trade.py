from typing import Optional
from pydantic import BaseModel

class ExitPositionResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    # VERIFY: assumed response shape
