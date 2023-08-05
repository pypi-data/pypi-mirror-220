# coding: utf-8

"""
    Fatture in Cloud API v2 - API Reference

    Connect your software with Fatture in Cloud, the invoicing platform chosen by more than 500.000 businesses in Italy.   The Fatture in Cloud API is based on REST, and makes possible to interact with the user related data prior authorization via OAuth2 protocol.  # noqa: E501

    The version of the OpenAPI document: 2.0.29
    Contact: info@fattureincloud.it
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg


class CashbookEntryKind(str, Enum):
    """
    Cashbook kind
    """

    """
    allowed enum values
    """
    CASHBOOK = "cashbook"
    ISSUED_DOCUMENT = "issued_document"
    RECEIVED_DOCUMENT = "received_document"
    TAX = "tax"
    RECEIPT = "receipt"

    @classmethod
    def from_json(cls, json_str: str) -> CashbookEntryKind:
        """Create an instance of CashbookEntryKind from a JSON string"""
        return CashbookEntryKind(json.loads(json_str))
