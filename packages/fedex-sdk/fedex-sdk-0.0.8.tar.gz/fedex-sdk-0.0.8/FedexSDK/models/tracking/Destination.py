from pydantic import BaseModel

from .LocationContactAndAddress import LocationContactAndAddress

class DestinationLocation(BaseModel):
    locationContactAndAddress: LocationContactAndAddress
    locationType: str


class LastUpdatedDestinationAddress(BaseModel):
    city: str
    stateOrProvinceCode: str
    countryCode: str
    residential: bool
    countryName: str