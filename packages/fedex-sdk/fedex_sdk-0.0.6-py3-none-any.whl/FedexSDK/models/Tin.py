from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel

@dataclass
class TinType:
    Personal_National: str = "PERSONAL_NATIONAL"
    Personal_State: str = "PERSONAL_STATE"
    Federal: str = "FEDERAL"
    Business_National: str = "BUSINESS_NATIONAL"
    Business_State: str = "BUSINESS_STATE"
    Business_Union: str = "BUSINESS_UNION"
    
class Tin(BaseModel):
    number: Optional[str]
    tinType: Optional[TinType]
    usage: Optional[str]
    effectiveDate: Optional[str]
    expirationDate: Optional[str]    
    
