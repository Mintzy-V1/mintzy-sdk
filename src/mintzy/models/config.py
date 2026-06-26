from typing import Optional, Dict, Any
from pydantic import BaseModel

class SavedConfiguration(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    configuration: Dict[str, Any]
    # VERIFY: assumed response shape

class ConfigurationResponse(BaseModel):
    success: bool
    data: SavedConfiguration
    # VERIFY: assumed response shape
