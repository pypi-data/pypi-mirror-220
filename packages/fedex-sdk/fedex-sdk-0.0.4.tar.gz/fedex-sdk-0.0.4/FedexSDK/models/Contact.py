from typing import Optional
from pydantic import BaseModel, root_validator, validator

class Contact(BaseModel):
    personName: str = ""
    emailAddress: str = ""
    phoneExtension: str = ""
    companyName: str = ""
    phoneNumber: str
    
    
    @root_validator
    @classmethod
    def person_name_and_company_name_required_validate(cls, data):
        if data["personName"] == None and data["companyName"] == None:
            raise ValueError("Either the companyName or personName is mandatory")
        return data
        
    @validator("personName")
    @classmethod
    def person_name_validate(cls, value):
        if value is not None and len(value) > 70:
            raise ValueError(
                "Please Max 70 Character For Person Name"
            )
        return value
            
    @validator("emailAddress")
    @classmethod
    def emailAddress_validate(cls, value):
        if value is not None and len(value) > 80:
            raise ValueError(
                "Please Max 80 Character For Email Address"
            )
        return value
            
    @validator("phoneExtension")
    @classmethod
    def phoneExtension_validate(cls, value):
        if value is not None and len(value) > 6:
            raise ValueError(
                "Please Max 6 Character For Phone Extension"
            )
        return value
    
    @validator("companyName")
    @classmethod
    def companyName_validate(cls, value):
        if value is not None and len(value) > 35:
            raise ValueError(
                "Please Max 35 Character For Company Name Extension"
            )
        return value
    
    @validator("phoneNumber")
    @classmethod
    def phoneNumber_validate(cls, value):
        if value is not None:
            if len(value) > 15:
                
                raise ValueError(
                    "Please Max 15 Character For Phone Number"
                )
            elif len(value) < 10:
                raise ValueError(
                    "Please Min. 15 Character For Phone Number"
                )
        return value