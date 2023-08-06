from typing import Dict, Any
from .Address import Address
from pydantic import BaseModel

class ShipperInformation(BaseModel):
    contact: Dict[str, Any]
    address: Address