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
from pydantic import BaseModel, Field, StrictInt, StrictStr
from fattureincloud_python_sdk.models.supplier_type import SupplierType


class Supplier(BaseModel):
    """
    Supplier
    """

    id: Optional[StrictInt] = Field(None, description="Supplier id")
    code: Optional[StrictStr] = Field(None, description="Supplier code")
    name: Optional[StrictStr] = Field(None, description="Supplier name")
    type: Optional[SupplierType] = None
    first_name: Optional[StrictStr] = Field(None, description="Supplier first name")
    last_name: Optional[StrictStr] = Field(None, description="Supplier last name")
    contact_person: Optional[StrictStr] = Field(
        None, description="Supplier contact person"
    )
    vat_number: Optional[StrictStr] = Field(None, description="Supplier vat number")
    tax_code: Optional[StrictStr] = Field(None, description="Supplier tax code")
    address_street: Optional[StrictStr] = Field(
        None, description="Supplier street address"
    )
    address_postal_code: Optional[StrictStr] = Field(
        None, description="Supplier postal code"
    )
    address_city: Optional[StrictStr] = Field(None, description="Supplier city")
    address_province: Optional[StrictStr] = Field(None, description="Supplier province")
    address_extra: Optional[StrictStr] = Field(
        None, description="Supplier address extra info"
    )
    country: Optional[StrictStr] = Field(None, description="Supplier country")
    email: Optional[StrictStr] = Field(None, description="Supplier email")
    certified_email: Optional[StrictStr] = Field(
        None, description="Supplier certified email"
    )
    phone: Optional[StrictStr] = Field(None, description="Supplier phone")
    fax: Optional[StrictStr] = Field(None, description="Supplier fax")
    notes: Optional[StrictStr] = Field(None, description="Supplier extra notes")
    bank_iban: Optional[StrictStr] = Field(None, description="Supplier bank IBAN")
    created_at: Optional[StrictStr] = Field(None, description="Supplier creation date")
    updated_at: Optional[StrictStr] = Field(
        None, description="Supplier last update date"
    )
    __properties = [
        "id",
        "code",
        "name",
        "type",
        "first_name",
        "last_name",
        "contact_person",
        "vat_number",
        "tax_code",
        "address_street",
        "address_postal_code",
        "address_city",
        "address_province",
        "address_extra",
        "country",
        "email",
        "certified_email",
        "phone",
        "fax",
        "notes",
        "bank_iban",
        "created_at",
        "updated_at",
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
    def from_json(cls, json_str: str) -> Supplier:
        """Create an instance of Supplier from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Supplier:
        """Create an instance of Supplier from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Supplier.parse_obj(obj)

        _obj = Supplier.parse_obj(
            {
                "id": obj.get("id") if obj.get("id") is not None else None,
                "code": obj.get("code") if obj.get("code") is not None else None,
                "name": obj.get("name") if obj.get("name") is not None else None,
                "type": obj.get("type"),
                "first_name": obj.get("first_name")
                if obj.get("first_name") is not None
                else None,
                "last_name": obj.get("last_name")
                if obj.get("last_name") is not None
                else None,
                "contact_person": obj.get("contact_person")
                if obj.get("contact_person") is not None
                else None,
                "vat_number": obj.get("vat_number")
                if obj.get("vat_number") is not None
                else None,
                "tax_code": obj.get("tax_code")
                if obj.get("tax_code") is not None
                else None,
                "address_street": obj.get("address_street")
                if obj.get("address_street") is not None
                else None,
                "address_postal_code": obj.get("address_postal_code")
                if obj.get("address_postal_code") is not None
                else None,
                "address_city": obj.get("address_city")
                if obj.get("address_city") is not None
                else None,
                "address_province": obj.get("address_province")
                if obj.get("address_province") is not None
                else None,
                "address_extra": obj.get("address_extra")
                if obj.get("address_extra") is not None
                else None,
                "country": obj.get("country")
                if obj.get("country") is not None
                else None,
                "email": obj.get("email") if obj.get("email") is not None else None,
                "certified_email": obj.get("certified_email")
                if obj.get("certified_email") is not None
                else None,
                "phone": obj.get("phone") if obj.get("phone") is not None else None,
                "fax": obj.get("fax") if obj.get("fax") is not None else None,
                "notes": obj.get("notes") if obj.get("notes") is not None else None,
                "bank_iban": obj.get("bank_iban")
                if obj.get("bank_iban") is not None
                else None,
                "created_at": obj.get("created_at")
                if obj.get("created_at") is not None
                else None,
                "updated_at": obj.get("updated_at")
                if obj.get("updated_at") is not None
                else None,
            }
        )
        return _obj
