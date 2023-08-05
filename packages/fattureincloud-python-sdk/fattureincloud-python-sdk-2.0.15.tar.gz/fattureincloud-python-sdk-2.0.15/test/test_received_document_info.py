"""
    Fatture in Cloud API v2 - API Reference

    Connect your software with Fatture in Cloud, the invoicing platform chosen by more than 400.000 businesses in Italy.   The Fatture in Cloud API is based on REST, and makes possible to interact with the user related data prior authorization via OAuth2 protocol.  # noqa: E501

    The version of the OpenAPI document: 2.0.9
    Contact: info@fattureincloud.it
    Generated by: https://openapi-generator.tech
"""


import json
import sys
import unittest

import fattureincloud_python_sdk
from functions import json_serial
from functions import create_from_json
from fattureincloud_python_sdk.models.currency import Currency
from fattureincloud_python_sdk.models.payment_account import PaymentAccount
from fattureincloud_python_sdk.models.received_document_info_default_values import (
    ReceivedDocumentInfoDefaultValues,
)
from fattureincloud_python_sdk.models.received_document_info_items_default_values import (
    ReceivedDocumentInfoItemsDefaultValues,
)
from fattureincloud_python_sdk.models.vat_type import VatType

globals()["Currency"] = Currency
globals()["PaymentAccount"] = PaymentAccount
globals()["ReceivedDocumentInfoDefaultValues"] = ReceivedDocumentInfoDefaultValues
globals()[
    "ReceivedDocumentInfoItemsDefaultValues"
] = ReceivedDocumentInfoItemsDefaultValues
globals()["VatType"] = VatType
from fattureincloud_python_sdk.models.received_document_info import ReceivedDocumentInfo


class TestReceivedDocumentInfo(unittest.TestCase):
    """ReceivedDocumentInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReceivedDocumentInfo(self):
        """Test ReceivedDocumentInfo"""
        model = ReceivedDocumentInfo(
            default_values=ReceivedDocumentInfoDefaultValues(detailed=True),
            items_default_values=ReceivedDocumentInfoItemsDefaultValues(vat=22.0),
            countries_list=["IT", "US"],
            payment_accounts_list=[PaymentAccount(id=1, name="bank")],
            categories_list=["cat5", "cat6"],
            vat_types_list=[VatType(value=22.0)],
        )
        expected_json = '{"default_values": {"detailed": true}, "items_default_values": {"vat": 22.0}, "countries_list": ["IT", "US"], "categories_list": ["cat5", "cat6"], "payment_accounts_list": [{"id": 1, "name": "bank"}], "vat_types_list": [{"value": 22.0}]}'
        actual_json = json.dumps(model.to_dict(), default=json_serial)
        assert actual_json == expected_json


if __name__ == "__main__":
    unittest.main()
