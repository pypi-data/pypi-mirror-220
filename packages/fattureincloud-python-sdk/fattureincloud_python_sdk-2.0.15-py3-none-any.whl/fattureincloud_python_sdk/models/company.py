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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr, conlist
from fattureincloud_python_sdk.models.company_type import CompanyType
from fattureincloud_python_sdk.models.controlled_company import ControlledCompany


class Company(BaseModel):
    """
    Company
    """

    id: Optional[StrictInt] = Field(None, description="Company id")
    name: Optional[StrictStr] = Field(None, description="Company name")
    type: Optional[CompanyType] = None
    access_token: Optional[StrictStr] = Field(
        None,
        description="Company authentication token for this company. [Only if type=company]",
    )
    controlled_companies: Optional[conlist(ControlledCompany)] = Field(
        None,
        description="Company list of controlled companies [Only if type=accountant]",
    )
    connection_id: Optional[StrictInt] = Field(
        None, description="Company connection id"
    )
    tax_code: Optional[StrictStr] = Field(None, description="Company tax code")
    __properties = [
        "id",
        "name",
        "type",
        "access_token",
        "controlled_companies",
        "connection_id",
        "tax_code",
    ]

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
    def from_json(cls, json_str: str) -> Company:
        """Create an instance of Company from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in controlled_companies (list)
        _items = []
        if self.controlled_companies:
            for _item in self.controlled_companies:
                if _item:
                    _items.append(_item.to_dict())
            _dict["controlled_companies"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Company:
        """Create an instance of Company from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Company.parse_obj(obj)

        _obj = Company.parse_obj(
            {
                "id": obj.get("id") if obj.get("id") is not None else None,
                "name": obj.get("name") if obj.get("name") is not None else None,
                "type": obj.get("type"),
                "access_token": obj.get("access_token")
                if obj.get("access_token") is not None
                else None,
                "controlled_companies": [
                    ControlledCompany.from_dict(_item)
                    for _item in obj.get("controlled_companies")
                ]
                if obj.get("controlled_companies") is not None
                else None,
                "connection_id": obj.get("connection_id")
                if obj.get("connection_id") is not None
                else None,
                "tax_code": obj.get("tax_code")
                if obj.get("tax_code") is not None
                else None,
            }
        )
        return _obj
