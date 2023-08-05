"""
    Fatture in Cloud API v2 - API Reference

    Connect your software with Fatture in Cloud, the invoicing platform chosen by more than 400.000 businesses in Italy.   The Fatture in Cloud API is based on REST, and makes possible to interact with the user related data prior authorization via OAuth2 protocol.  # noqa: E501

    The version of the OpenAPI document: 2.0.9
    Contact: info@fattureincloud.it
    Generated by: https://openapi-generator.tech
"""


import unittest
import unittest.mock
import fattureincloud_python_sdk
import functions
from fattureincloud_python_sdk.rest import RESTResponse
from fattureincloud_python_sdk.api.suppliers_api import SuppliersApi
from fattureincloud_python_sdk.models.create_supplier_response import (
    CreateSupplierResponse,
)
from fattureincloud_python_sdk.models.supplier import Supplier
from fattureincloud_python_sdk.models.supplier_type import SupplierType
from fattureincloud_python_sdk.models.get_supplier_response import GetSupplierResponse
from fattureincloud_python_sdk.models.list_suppliers_response import (
    ListSuppliersResponse,
)
from fattureincloud_python_sdk.models.modify_supplier_response import (
    ModifySupplierResponse,
)  # noqa: E501


class TestSuppliersApi(unittest.TestCase):
    """SuppliersApi unit test stubs"""

    def setUp(self):
        self.api = SuppliersApi()

    def tearDown(self):
        pass

    def test_create_supplier(self):
        resp = {
            "status": 200,
            "data": b'{"data": {"id": 1, "code": "123", "name": "Rossi S.r.l.", "type": "company", "first_name": "first_name_example", "last_name": "last_name_example", "contact_person": "contact_person_example", "vat_number": "IT01234567890", "tax_code": "RSSMRA44A12E890Q", "address_street": "Via dei tigli, 12", "address_postal_code": "24010", "address_city": "Bergamo", "address_province": "BG", "address_extra": "address_extra_example", "country": "Italia", "email": "mario.rossi@example.it", "certified_email": "mario.rossi@pec.example.it", "phone": "phone_example", "fax": "fax_example", "notes": "notes_example", "created_at": "created_at_example", "updated_at": "updated_at_example"}}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.post_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = CreateSupplierResponse(
            data=Supplier(
                id=2,
                code="123",
                name="Rossi S.r.l.",
                type=SupplierType("company"),
                first_name="first_name_example",
                last_name="last_name_example",
                contact_person="contact_person_example",
                vat_number="IT01234567890",
                tax_code="RSSMRA44A12E890Q",
                address_street="Via dei tigli, 12",
                address_postal_code="24010",
                address_city="Bergamo",
                address_province="BG",
                address_extra="address_extra_example",
                country="Italia",
                email="mario.rossi@example.it",
                certified_email="mario.rossi@pec.example.it",
                phone="phone_example",
                fax="fax_example",
                notes="notes_example",
                created_at="created_at_example",
                updated_at="updated_at_example",
            )
        )
        actual = self.api.create_supplier(2)
        actual.data.id = 2
        assert actual == expected

    def test_delete_supplier(self):
        resp = {"status": 200, "data": b"{}", "reason": "OK"}

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.delete_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        actual = self.api.delete_supplier(2, 12345)
        assert actual == None

    def test_get_supplier(self):
        resp = {
            "status": 200,
            "data": b'{"data": {"id": 1, "code": "123", "name": "Rossi S.r.l.", "type": "company", "first_name": "first_name_example", "last_name": "last_name_example", "contact_person": "contact_person_example", "vat_number": "IT01234567890", "tax_code": "RSSMRA44A12E890Q", "address_street": "Via dei tigli, 12", "address_postal_code": "24010", "address_city": "Bergamo", "address_province": "BG", "address_extra": "address_extra_example", "country": "Italia", "email": "mario.rossi@example.it", "certified_email": "mario.rossi@pec.example.it", "phone": "phone_example", "fax": "fax_example", "notes": "notes_example", "created_at": "created_at_example", "updated_at": "updated_at_example"}}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.get_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = GetSupplierResponse(
            data=Supplier(
                id=2,
                code="123",
                name="Rossi S.r.l.",
                type=SupplierType("company"),
                first_name="first_name_example",
                last_name="last_name_example",
                contact_person="contact_person_example",
                vat_number="IT01234567890",
                tax_code="RSSMRA44A12E890Q",
                address_street="Via dei tigli, 12",
                address_postal_code="24010",
                address_city="Bergamo",
                address_province="BG",
                address_extra="address_extra_example",
                country="Italia",
                email="mario.rossi@example.it",
                certified_email="mario.rossi@pec.example.it",
                phone="phone_example",
                fax="fax_example",
                notes="notes_example",
                created_at="created_at_example",
                updated_at="updated_at_example",
            )
        )
        actual = self.api.get_supplier(2, 12345)
        actual.data.id = 2
        assert actual == expected

    def test_list_suppliers(self):
        resp = {
            "status": 200,
            "data": b'{"data": [{"id": 1, "code": "123", "name": "Rossi S.r.l.", "type": "company", "first_name": "first_name_example", "last_name": "last_name_example", "contact_person": "contact_person_example", "vat_number": "IT01234567890", "tax_code": "RSSMRA44A12E890Q", "address_street": "Via dei tigli, 12", "address_postal_code": "24010", "address_city": "Bergamo", "address_province": "BG", "address_extra": "address_extra_example", "country": "Italia", "email": "mario.rossi@example.it", "certified_email": "mario.rossi@pec.example.it", "phone": "phone_example", "fax": "fax_example", "notes": "notes_example", "created_at": "created_at_example", "updated_at": "updated_at_example"}, {"id": 1, "code": "123", "name": "Rossi S.r.l.", "type": "company", "first_name": "first_name_example", "last_name": "last_name_example", "contact_person": "contact_person_example", "vat_number": "IT01234567890", "tax_code": "RSSMRA44A12E890Q", "address_street": "Via dei tigli, 12", "address_postal_code": "24010", "address_city": "Bergamo", "address_province": "BG", "address_extra": "address_extra_example", "country": "Italia", "email": "mario.rossi@example.it", "certified_email": "mario.rossi@pec.example.it", "phone": "phone_example", "fax": "fax_example", "notes": "notes_example", "created_at": "created_at_example", "updated_at": "updated_at_example"}]}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.get_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = ListSuppliersResponse(
            data=[
                Supplier(
                    id=2,
                    code="123",
                    name="Rossi S.r.l.",
                    type=SupplierType("company"),
                    first_name="first_name_example",
                    last_name="last_name_example",
                    contact_person="contact_person_example",
                    vat_number="IT01234567890",
                    tax_code="RSSMRA44A12E890Q",
                    address_street="Via dei tigli, 12",
                    address_postal_code="24010",
                    address_city="Bergamo",
                    address_province="BG",
                    address_extra="address_extra_example",
                    country="Italia",
                    email="mario.rossi@example.it",
                    certified_email="mario.rossi@pec.example.it",
                    phone="phone_example",
                    fax="fax_example",
                    notes="notes_example",
                    created_at="created_at_example",
                    updated_at="updated_at_example",
                ),
                Supplier(
                    id=2,
                    code="123",
                    name="Rossi S.r.l.",
                    type=SupplierType("company"),
                    first_name="first_name_example",
                    last_name="last_name_example",
                    contact_person="contact_person_example",
                    vat_number="IT01234567890",
                    tax_code="RSSMRA44A12E890Q",
                    address_street="Via dei tigli, 12",
                    address_postal_code="24010",
                    address_city="Bergamo",
                    address_province="BG",
                    address_extra="address_extra_example",
                    country="Italia",
                    email="mario.rossi@example.it",
                    certified_email="mario.rossi@pec.example.it",
                    phone="phone_example",
                    fax="fax_example",
                    notes="notes_example",
                    created_at="created_at_example",
                    updated_at="updated_at_example",
                ),
            ]
        )
        actual = self.api.list_suppliers(2)
        actual.data[0].id = 2
        actual.data[1].id = 2
        assert actual == expected

    def test_modify_supplier(self):
        resp = {
            "status": 200,
            "data": b'{"data": {"id": 1, "code": "123", "name": "Rossi S.r.l.", "type": "company", "first_name": "first_name_example", "last_name": "last_name_example", "contact_person": "contact_person_example", "vat_number": "IT01234567890", "tax_code": "RSSMRA44A12E890Q", "address_street": "Via dei tigli, 12", "address_postal_code": "24010", "address_city": "Bergamo", "address_province": "BG", "address_extra": "address_extra_example", "country": "Italia", "email": "mario.rossi@example.it", "certified_email": "mario.rossi@pec.example.it", "phone": "phone_example", "fax": "fax_example", "notes": "notes_example", "created_at": "created_at_example", "updated_at": "updated_at_example"}}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.put_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = ModifySupplierResponse(
            data=Supplier(
                id=2,
                code="123",
                name="Rossi S.r.l.",
                type=SupplierType("company"),
                first_name="first_name_example",
                last_name="last_name_example",
                contact_person="contact_person_example",
                vat_number="IT01234567890",
                tax_code="RSSMRA44A12E890Q",
                address_street="Via dei tigli, 12",
                address_postal_code="24010",
                address_city="Bergamo",
                address_province="BG",
                address_extra="address_extra_example",
                country="Italia",
                email="mario.rossi@example.it",
                certified_email="mario.rossi@pec.example.it",
                phone="phone_example",
                fax="fax_example",
                notes="notes_example",
                created_at="created_at_example",
                updated_at="updated_at_example",
            )
        )
        actual = self.api.modify_supplier(2, 12345)
        actual.data.id = 2
        assert actual == expected


if __name__ == "__main__":
    unittest.main()
