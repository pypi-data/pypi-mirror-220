from pydantic import BaseModel
from typing import List
from .DeliveryOptionEligiblityDetail import DeliveryOptionEligibilityDetail


class DeliveryDetails(BaseModel):
    deliveryAttempts: str
    deliveryOptionEligibilityDetails: List[DeliveryOptionEligibilityDetail]
    destinationServiceArea: str