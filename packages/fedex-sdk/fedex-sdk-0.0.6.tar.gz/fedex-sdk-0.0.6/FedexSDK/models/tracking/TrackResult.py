from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .ServiceCommitMessage import ServiceCommitMessage
from .Destination import DestinationLocation, LastUpdatedDestinationAddress
from .OriginLocation import OriginLocation
from .DeliveryDetails import DeliveryDetails
from .SpecialHandling import SpecialHandling
from .DateAndTime import DateAndTime
from .LatestStatusDetail import LatestStatusDetail
from .RecipientInformation import RecipientInformation
from .ShipperInformation import ShipperInformation
from .AdditionalTrackingInfo import AdditionalTrackingInfo
from .TrackingNumberInfo import TrackingNumberInfo
from .Window import EstimatedDeliveryTimeWindow, StandardTransitTimeWindow
from .ServiceDetail import ServiceDetail
from .ScanEvent import ScanEvent
from .PackageDetails import PackageDetails
from .ShipmentDetails import ShipmentDetails

class TrackResult(BaseModel):
    trackingNumberInfo: TrackingNumberInfo
    additionalTrackingInfo: AdditionalTrackingInfo
    shipperInformation: ShipperInformation
    recipientInformation: RecipientInformation
    latestStatusDetail: LatestStatusDetail
    dateAndTimes: List[DateAndTime]
    availableImages: List
    specialHandlings: List[SpecialHandling]
    packageDetails: PackageDetails
    shipmentDetails: ShipmentDetails
    scanEvents: List[ScanEvent]
    availableNotifications: List[str]
    deliveryDetails: DeliveryDetails
    originLocation: OriginLocation
    destinationLocation: DestinationLocation
    lastUpdatedDestinationAddress: LastUpdatedDestinationAddress
    serviceCommitMessage: Optional[ServiceCommitMessage]
    serviceDetail: ServiceDetail
    standardTransitTimeWindow: StandardTransitTimeWindow
    estimatedDeliveryTimeWindow: EstimatedDeliveryTimeWindow
    goodsClassificationCode: str
    returnDetail: Dict[str, Any]

class CompleteTrackResult(BaseModel):
    trackingNumber: str
    trackResults: List[TrackResult]

class Output(BaseModel):
    completeTrackResults: List[CompleteTrackResult]
    
class TrackResponse(BaseModel):
    transactionId: str
    output: Output