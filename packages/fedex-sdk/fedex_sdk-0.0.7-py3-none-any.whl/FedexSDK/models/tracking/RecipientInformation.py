from typing import Dict, Any
from pydantic import BaseModel
from .Address import Address

class RecipientInformation(BaseModel):
    contact: Dict[str, Any]
    address: Address