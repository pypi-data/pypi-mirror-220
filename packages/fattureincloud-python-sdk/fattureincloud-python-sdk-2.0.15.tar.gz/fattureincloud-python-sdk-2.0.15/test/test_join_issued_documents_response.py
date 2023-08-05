"""
    Fatture in Cloud API v2 - API Reference

    Connect your software with Fatture in Cloud, the invoicing platform chosen by more than 500.000 businesses in Italy.   The Fatture in Cloud API is based on REST, and makes possible to interact with the user related data prior authorization via OAuth2 protocol.  # noqa: E501

    The version of the OpenAPI document: 2.0.22
    Contact: info@fattureincloud.it
    Generated by: https://openapi-generator.tech
"""


import datetime
import json
import sys
import unittest

import fattureincloud_python_sdk
from fattureincloud_python_sdk.models.issued_document import IssuedDocument
from fattureincloud_python_sdk.models.entity import Entity
from fattureincloud_python_sdk.models.issued_document_type import IssuedDocumentType
from fattureincloud_python_sdk.models.payment_method import PaymentMethod
from fattureincloud_python_sdk.models.issued_document_options import (
    IssuedDocumentOptions,
)
from functions import json_serial

globals()["IssuedDocument"] = IssuedDocument
globals()["IssuedDocumentOptions"] = IssuedDocumentOptions
from fattureincloud_python_sdk.models.join_issued_documents_response import (
    JoinIssuedDocumentsResponse,
)


class TestJoinIssuedDocumentsResponse(unittest.TestCase):
    """JoinIssuedDocumentsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testJoinIssuedDocumentsResponse(self):
        """Test JoinIssuedDocumentsResponse"""
        model = JoinIssuedDocumentsResponse(
            data=IssuedDocument(
                id=1,
                type=IssuedDocumentType("invoice"),
                entity=Entity(
                    id=54321,
                    name="Mary Red S.r.L.",
                    vat_number="IT05432181211",
                    tax_code="IT05432181211",
                    address_street="Corso impero, 66",
                    address_postal_code="20900",
                    address_city="Milano",
                    address_province="MI",
                    address_extra="",
                    country="Italia",
                    certified_email="mary@pec.red.com",
                    ei_code="ABCXCR1",
                ),
                number=1,
                numeration="/A",
                date=datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
                year=1,
                subject="subject_example",
                visible_subject="visible_subject_example",
                rc_center="rc_center_example",
                notes="notes_example",
                rivalsa=0.0,
                cassa=0.0,
                cassa_taxable=0.0,
                amount_cassa_taxable=3.14,
                cassa2=0.0,
                cassa2_taxable=0.0,
                amount_cassa2_taxable=3.14,
                global_cassa_taxable=0.0,
                amount_global_cassa_taxable=3.14,
            ),
            options=IssuedDocumentOptions(create_from=["12345", "54321"]),
        )
        expected_json = '{"data": {"id": 1, "entity": {"id": 54321, "name": "Mary Red S.r.L.", "vat_number": "IT05432181211", "tax_code": "IT05432181211", "address_street": "Corso impero, 66", "address_postal_code": "20900", "address_city": "Milano", "address_province": "MI", "address_extra": "", "country": "Italia", "certified_email": "mary@pec.red.com", "ei_code": "ABCXCR1"}, "type": "invoice", "number": 1, "numeration": "/A", "date": "2022-01-01", "year": 1, "subject": "subject_example", "visible_subject": "visible_subject_example", "rc_center": "rc_center_example", "notes": "notes_example", "rivalsa": 0.0, "cassa": 0.0, "cassa_taxable": 0.0, "amount_cassa_taxable": 3.14, "cassa2": 0.0, "cassa2_taxable": 0.0, "amount_cassa2_taxable": 3.14, "global_cassa_taxable": 0.0, "amount_global_cassa_taxable": 3.14}, "options": {"create_from": ["12345", "54321"]}}'
        actual_json = json.dumps(model.to_dict(), default=json_serial)
        assert actual_json == expected_json


if __name__ == "__main__":
    unittest.main()
