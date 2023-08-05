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
from fattureincloud_python_sdk.api.products_api import ProductsApi
from fattureincloud_python_sdk.models.create_product_response import (
    CreateProductResponse,
)
from fattureincloud_python_sdk.models.get_product_response import GetProductResponse
from fattureincloud_python_sdk.models.list_products_response import ListProductsResponse
from fattureincloud_python_sdk.models.modify_product_response import (
    ModifyProductResponse,
)
from fattureincloud_python_sdk.models.product import Product
from fattureincloud_python_sdk.models.vat_type import VatType


class TestProductsApi(unittest.TestCase):
    """ProductsApi unit test stubs"""

    def setUp(self):
        self.api = ProductsApi()

    def tearDown(self):
        pass

    def test_create_product(self):
        resp = {
            "status": 200,
            "data": b'{"data": {"id": 1, "name": "name_example", "code": "code_example", "net_price": 3.14, "gross_price": 3.14, "use_gross_price": true, "default_vat": {"id": 1, "value": 22.0, "description": "Non imponibile art. 123", "notes": "IVA non imponibile ai sensi dell articolo 123, comma 2", "e_invoice": true, "ei_type": "2", "ei_description": "ei_description_example", "is_disabled": true}, "net_cost": 3.14, "measure": "measure_example", "description": "description_example", "category": "category_example", "notes": "notes_example", "in_stock": true, "stock_initial": 3.14, "average_cost": 3.14, "average_price": 3.14, "created_at": "created_at_example", "updated_at": "updated_at_example"}}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.post_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = CreateProductResponse(
            data=Product(
                id=2,
                name="name_example",
                code="code_example",
                net_price=3.14,
                gross_price=3.14,
                use_gross_price=True,
                default_vat=VatType(
                    id=1,
                    value=22.0,
                    description="Non imponibile art. 123",
                    notes="IVA non imponibile ai sensi dell articolo 123, comma 2",
                    e_invoice=True,
                    ei_type="2",
                    ei_description="ei_description_example",
                    is_disabled=True,
                ),
                net_cost=3.14,
                measure="measure_example",
                description="description_example",
                category="category_example",
                notes="notes_example",
                in_stock=True,
                stock_initial=3.14,
                average_cost=3.14,
                average_price=3.14,
                created_at="created_at_example",
                updated_at="updated_at_example",
            )
        )
        actual = self.api.create_product(2)
        actual.data.id = 2
        assert actual == expected

    def test_delete_product(self):
        resp = {"status": 200, "data": b"{}", "reason": "OK"}

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.delete_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        actual = self.api.delete_product(2, 12345)
        assert actual == None

    def test_get_product(self):
        resp = {
            "status": 200,
            "data": b'{"data": {"id": 1, "name": "name_example", "code": "code_example", "net_price": 3.14, "gross_price": 3.14, "use_gross_price": true, "default_vat": {"id": 1, "value": 22.0, "description": "Non imponibile art. 123", "notes": "IVA non imponibile ai sensi dell articolo 123, comma 2", "e_invoice": true, "ei_type": "2", "ei_description": "ei_description_example", "is_disabled": true}, "net_cost": 3.14, "measure": "measure_example", "description": "description_example", "category": "category_example", "notes": "notes_example", "in_stock": true, "stock_initial": 3.14, "average_cost": 3.14, "average_price": 3.14, "created_at": "created_at_example", "updated_at": "updated_at_example"}}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.get_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = GetProductResponse(
            data=Product(
                id=2,
                name="name_example",
                code="code_example",
                net_price=3.14,
                gross_price=3.14,
                use_gross_price=True,
                default_vat=VatType(
                    id=1,
                    value=22.0,
                    description="Non imponibile art. 123",
                    notes="IVA non imponibile ai sensi dell articolo 123, comma 2",
                    e_invoice=True,
                    ei_type="2",
                    ei_description="ei_description_example",
                    is_disabled=True,
                ),
                net_cost=3.14,
                measure="measure_example",
                description="description_example",
                category="category_example",
                notes="notes_example",
                in_stock=True,
                stock_initial=3.14,
                average_cost=3.14,
                average_price=3.14,
                created_at="created_at_example",
                updated_at="updated_at_example",
            )
        )
        actual = self.api.get_product(2, 12345)
        actual.data.id = 2
        assert actual == expected

    def test_list_products(self):
        resp = {
            "status": 200,
            "data": b'{"data": [{"id": 1, "name": "name_example", "code": "code_example", "net_price": 3.14, "gross_price": 3.14, "use_gross_price": true, "default_vat": {"id": 1, "value": 22.0, "description": "Non imponibile art. 123", "notes": "IVA non imponibile ai sensi dell articolo 123, comma 2", "e_invoice": true, "ei_type": "2", "ei_description": "ei_description_example", "is_disabled": true}, "net_cost": 3.14, "measure": "measure_example", "description": "description_example", "category": "category_example", "notes": "notes_example", "in_stock": true, "stock_initial": 3.14, "average_cost": 3.14, "average_price": 3.14, "created_at": "created_at_example", "updated_at": "updated_at_example"}, {"id": 1, "name": "name_example", "code": "code_example", "net_price": 3.14, "gross_price": 3.14, "use_gross_price": true, "default_vat": {"id": 1, "value": 22.0, "description": "Non imponibile art. 123", "notes": "IVA non imponibile ai sensi dell articolo 123, comma 2", "e_invoice": true, "ei_type": "2", "ei_description": "ei_description_example", "is_disabled": true}, "net_cost": 3.14, "measure": "measure_example", "description": "description_example", "category": "category_example", "notes": "notes_example", "in_stock": true, "stock_initial": 3.14, "average_cost": 3.14, "average_price": 3.14, "created_at": "created_at_example", "updated_at": "updated_at_example"}]}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.get_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = ListProductsResponse(
            data=[
                Product(
                    id=2,
                    name="name_example",
                    code="code_example",
                    net_price=3.14,
                    gross_price=3.14,
                    use_gross_price=True,
                    default_vat=VatType(
                        id=1,
                        value=22.0,
                        description="Non imponibile art. 123",
                        notes="IVA non imponibile ai sensi dell articolo 123, comma 2",
                        e_invoice=True,
                        ei_type="2",
                        ei_description="ei_description_example",
                        is_disabled=True,
                    ),
                    net_cost=3.14,
                    measure="measure_example",
                    description="description_example",
                    category="category_example",
                    notes="notes_example",
                    in_stock=True,
                    stock_initial=3.14,
                    average_cost=3.14,
                    average_price=3.14,
                    created_at="created_at_example",
                    updated_at="updated_at_example",
                ),
                Product(
                    id=2,
                    name="name_example",
                    code="code_example",
                    net_price=3.14,
                    gross_price=3.14,
                    use_gross_price=True,
                    default_vat=VatType(
                        id=1,
                        value=22.0,
                        description="Non imponibile art. 123",
                        notes="IVA non imponibile ai sensi dell articolo 123, comma 2",
                        e_invoice=True,
                        ei_type="2",
                        ei_description="ei_description_example",
                        is_disabled=True,
                    ),
                    net_cost=3.14,
                    measure="measure_example",
                    description="description_example",
                    category="category_example",
                    notes="notes_example",
                    in_stock=True,
                    stock_initial=3.14,
                    average_cost=3.14,
                    average_price=3.14,
                    created_at="created_at_example",
                    updated_at="updated_at_example",
                ),
            ]
        )
        actual = self.api.list_products(2)
        actual.data[0].id = 2
        actual.data[1].id = 2
        assert actual == expected

    def test_modify_product(self):
        resp = {
            "status": 200,
            "data": b'{"data": {"id": 1, "name": "name_example", "code": "code_example", "net_price": 3.14, "gross_price": 3.14, "use_gross_price": true, "default_vat": {"id": 1, "value": 22.0, "description": "Non imponibile art. 123", "notes": "IVA non imponibile ai sensi dell articolo 123, comma 2", "e_invoice": true, "ei_type": "2", "ei_description": "ei_description_example", "is_disabled": true}, "net_cost": 3.14, "measure": "measure_example", "description": "description_example", "category": "category_example", "notes": "notes_example", "in_stock": true, "stock_initial": 3.14, "average_cost": 3.14, "average_price": 3.14, "created_at": "created_at_example", "updated_at": "updated_at_example"}}',
            "reason": "OK",
        }

        mock_resp = RESTResponse(functions.Dict2Class(resp))
        mock_resp.getheader = unittest.mock.MagicMock(return_value=None)
        mock_resp.getheaders = unittest.mock.MagicMock(return_value=None)

        self.api.api_client.rest_client.put_request = unittest.mock.MagicMock(
            return_value=mock_resp
        )
        expected = ModifyProductResponse(
            data=Product(
                id=2,
                name="name_example",
                code="code_example",
                net_price=3.14,
                gross_price=3.14,
                use_gross_price=True,
                default_vat=VatType(
                    id=1,
                    value=22.0,
                    description="Non imponibile art. 123",
                    notes="IVA non imponibile ai sensi dell articolo 123, comma 2",
                    e_invoice=True,
                    ei_type="2",
                    ei_description="ei_description_example",
                    is_disabled=True,
                ),
                net_cost=3.14,
                measure="measure_example",
                description="description_example",
                category="category_example",
                notes="notes_example",
                in_stock=True,
                stock_initial=3.14,
                average_cost=3.14,
                average_price=3.14,
                created_at="created_at_example",
                updated_at="updated_at_example",
            )
        )
        actual = self.api.modify_product(2, 12345)
        actual.data.id = 2
        assert actual == expected


if __name__ == "__main__":
    unittest.main()
