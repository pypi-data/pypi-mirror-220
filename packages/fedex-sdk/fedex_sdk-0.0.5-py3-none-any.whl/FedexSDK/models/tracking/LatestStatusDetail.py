from pydantic import BaseModel
from .DelayDetail import DelayDetail
from .ScanLocation import ScanLocation

class LatestStatusDetail(BaseModel):
    code: str
    derivedCode: str
    statusByLocale: str
    description: str
    scanLocation: ScanLocation
    delayDetail: DelayDetail