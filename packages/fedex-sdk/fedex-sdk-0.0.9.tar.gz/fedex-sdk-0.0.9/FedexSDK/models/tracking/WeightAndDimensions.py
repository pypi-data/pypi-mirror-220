from typing import List
from pydantic import BaseModel

class Dimension(BaseModel):
    length: int
    width: int
    height: int
    units: str

class WeightItem(BaseModel):
    value: str
    unit: str

class WeightAndDimensions(BaseModel):
    weight: List[WeightItem]
    dimensions: List[Dimension]