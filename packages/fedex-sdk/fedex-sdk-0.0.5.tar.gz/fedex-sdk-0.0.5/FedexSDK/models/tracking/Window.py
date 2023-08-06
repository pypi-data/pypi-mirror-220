from pydantic import BaseModel
from typing import Dict, Any

class Window(BaseModel):
    ends: str


class StandardTransitTimeWindow(BaseModel):
    window: Window


class EstimatedDeliveryTimeWindow(BaseModel):
    window: Dict[str, Any]