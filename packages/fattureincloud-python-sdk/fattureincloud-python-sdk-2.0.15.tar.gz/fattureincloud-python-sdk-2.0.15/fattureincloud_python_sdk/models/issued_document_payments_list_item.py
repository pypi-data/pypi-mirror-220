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

from datetime import date
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt
from fattureincloud_python_sdk.models.issued_document_payments_list_item_payment_terms import (
    IssuedDocumentPaymentsListItemPaymentTerms,
)
from fattureincloud_python_sdk.models.issued_document_status import IssuedDocumentStatus
from fattureincloud_python_sdk.models.payment_account import PaymentAccount


class IssuedDocumentPaymentsListItem(BaseModel):
    """
    IssuedDocumentPaymentsListItem
    """

    id: Optional[StrictInt] = Field(None, description="Issued document payment item id")
    due_date: Optional[date] = Field(
        None, description="Issued document payment due date"
    )
    amount: Optional[Union[StrictFloat, StrictInt]] = Field(
        None, description="Issued document payment amount"
    )
    status: Optional[IssuedDocumentStatus] = None
    payment_account: Optional[PaymentAccount] = None
    paid_date: Optional[date] = Field(
        None, description="Issued document payment date [Only if status is paid]"
    )
    ei_raw: Optional[Dict[str, Any]] = Field(
        None,
        description="Issued document payment advanced raw attributes for e-invoices",
    )
    payment_terms: Optional[IssuedDocumentPaymentsListItemPaymentTerms] = None
    __properties = [
        "id",
        "due_date",
        "amount",
        "status",
        "payment_account",
        "paid_date",
        "ei_raw",
        "payment_terms",
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
    def from_json(cls, json_str: str) -> IssuedDocumentPaymentsListItem:
        """Create an instance of IssuedDocumentPaymentsListItem from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of payment_account
        if self.payment_account:
            _dict["payment_account"] = self.payment_account.to_dict()
        # override the default output from pydantic by calling `to_dict()` of payment_terms
        if self.payment_terms:
            _dict["payment_terms"] = self.payment_terms.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssuedDocumentPaymentsListItem:
        """Create an instance of IssuedDocumentPaymentsListItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssuedDocumentPaymentsListItem.parse_obj(obj)

        _obj = IssuedDocumentPaymentsListItem.parse_obj(
            {
                "id": obj.get("id") if obj.get("id") is not None else None,
                "due_date": obj.get("due_date")
                if obj.get("due_date") is not None
                else None,
                "amount": float(obj.get("amount"))
                if obj.get("amount") is not None
                else None,
                "status": obj.get("status"),
                "payment_account": PaymentAccount.from_dict(obj.get("payment_account"))
                if obj.get("payment_account") is not None
                else None,
                "paid_date": obj.get("paid_date")
                if obj.get("paid_date") is not None
                else None,
                "ei_raw": obj.get("ei_raw") if obj.get("ei_raw") is not None else None,
                "payment_terms": IssuedDocumentPaymentsListItemPaymentTerms.from_dict(
                    obj.get("payment_terms")
                )
                if obj.get("payment_terms") is not None
                else None,
            }
        )
        return _obj
