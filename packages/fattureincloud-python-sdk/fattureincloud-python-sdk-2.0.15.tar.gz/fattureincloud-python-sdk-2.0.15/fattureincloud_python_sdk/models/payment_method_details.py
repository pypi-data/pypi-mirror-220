# coding: utf-8

"""
    Fatture in Cloud API v2 - API Reference

    Connect your software with Fatture in Cloud, the invoicing platform chosen by more than 500.000 businesses in Italy.   The Fatture in Cloud API is based on REST, and makes possible to interact with the user related data prior authorization via OAuth2 protocol.  # noqa: E501

    The version of the OpenAPI document: 2.0.29
    Contact: info@fattureincloud.it
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr


class PaymentMethodDetails(BaseModel):
    """
    PaymentMethodDetails
    """

    title: Optional[StrictStr] = Field(None, description="Payment method details title")
    description: Optional[StrictStr] = Field(
        None, description="Payment method details description"
    )
    __properties = ["title", "description"]

    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PaymentMethodDetails:
        """Create an instance of PaymentMethodDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PaymentMethodDetails:
        """Create an instance of PaymentMethodDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaymentMethodDetails.parse_obj(obj)

        _obj = PaymentMethodDetails.parse_obj(
            {
                "title": obj.get("title") if obj.get("title") is not None else None,
                "description": obj.get("description")
                if obj.get("description") is not None
                else None,
            }
        )
        return _obj
