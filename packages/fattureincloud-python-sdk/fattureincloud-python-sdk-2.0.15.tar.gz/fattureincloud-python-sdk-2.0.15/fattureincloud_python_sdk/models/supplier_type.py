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


class SupplierType(str, Enum):
    """
    Supplier type
    """

    """
    allowed enum values
    """
    COMPANY = "company"
    PERSON = "person"
    PA = "pa"
    CONDO = "condo"

    @classmethod
    def from_json(cls, json_str: str) -> SupplierType:
        """Create an instance of SupplierType from a JSON string"""
        return SupplierType(json.loads(json_str))
