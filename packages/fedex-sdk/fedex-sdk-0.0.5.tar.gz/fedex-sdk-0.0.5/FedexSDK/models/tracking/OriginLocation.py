from pydantic import BaseModel
from .LocationContactAndAddress import LocationContactAndAddress


class OriginLocation(BaseModel):
    locationContactAndAddress: LocationContactAndAddress
    locationId: str