import datetime
import json
import os
from dataclasses import dataclass
from requests_oauthlib import OAuth2Session
import requests
from FedexSDK.models import Request

@dataclass
class APIType:
    Production: str = "Production"
    Test: str = "Test"

@dataclass
class ImageType:
    Letter_Head: str = "LETTER_HEAD"
    Signature: str = "SIGNATURE"

class FedExSDK:

    def __init__(self, session: OAuth2Session) -> None:
        if not isinstance(session, OAuth2Session):
            raise Exception("Please Requests Session")
        
        self.session = session
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session.access_token}"
        }

    def create_shipment(self, request: Request, output_json_path: str):
        url = "https://apis.fedex.com/ship/v1/shipments"

        res = self.session.post(url, json=request.dict(), headers=self.headers)
        
        now_date = datetime.datetime.now()
        with open(f"{now_date.strftime('%d_%m_%Y_tracking_numbers.txt')}", "a") as f:
            f.write(
                f"{res.json()['output']['transactionShipments'][0]['shipmentDocuments'][0]['trackingNumber']}:{request.requestedShipment.recipients[0].contact.personName}\n"
            )
        
        json.dump(res.json(), open(output_json_path, "w", encoding="utf-8"), ensure_ascii=False)

    
    def add_image(self, reference_id: str, image_name: str, image_index: str, image_type: ImageType, image_path: str):
        name, ext = os.path.splitext(image_path)
        data = {
            "document": {
                "referenceId": reference_id,
                "name": image_name,
                "contentType": f"image/{ext}",
                "meta":{
                    "imageType": image_type,
                    "imageIndex": image_index
                }
            },
            "rules":{
                "workflowName":"LetterheadSignature"
            }
        }
        files = {
            "attachment": open(image_path, "rb").read()
        }
        url = "https://documentapi.prod.fedex.com/documents/v1/lhsimages/upload"
        
        headers = self.headers
        headers["Content-Type"] = "multipart/form-data"
        
        res = self.session.post(url, data=data, headers=headers, files=files)
        
    @classmethod
    def authorize(cls, client_id: str, client_secret: str, api_type: APIType = APIType.Test) -> OAuth2Session:
        if api_type == APIType.Production:
            url = "https://apis.fedex.com/oauth/token"
        elif api_type == APIType.Test:
            url = "https://apis.sandbox.fedex.com/oauth/token"
        else:
            raise ValueError("Please Correct APIType!")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.request("POST", url, data=data, headers=headers)
        return OAuth2Session(client_id=client_id, token=response.json())


