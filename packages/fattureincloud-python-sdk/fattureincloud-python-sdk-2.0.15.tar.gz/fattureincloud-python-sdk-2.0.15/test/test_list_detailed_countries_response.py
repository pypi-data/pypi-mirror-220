"""
    Fatture in Cloud API v2 - API Reference

    Connect your software with Fatture in Cloud, the invoicing platform chosen by more than 400.000 businesses in Italy.   The Fatture in Cloud API is based on REST, and makes possible to interact with the user related data prior authorization via OAuth2 protocol.  # noqa: E501

    The version of the OpenAPI document: 2.0.14
    Contact: info@fattureincloud.it
    Generated by: https://openapi-generator.tech
"""


import json
import sys
import unittest
from functions import json_serial
import fattureincloud_python_sdk
from fattureincloud_python_sdk.models.detailed_country import DetailedCountry

globals()["DetailedCountry"] = DetailedCountry
from fattureincloud_python_sdk.models.list_detailed_countries_response import (
    ListDetailedCountriesResponse,
)


class TestListDetailedCountriesResponse(unittest.TestCase):
    """ListDetailedCountriesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testListDetailedCountriesResponse(self):
        """Test ListDetailedCountriesResponse"""
        model = ListDetailedCountriesResponse(
            data=[
                DetailedCountry(
                    name="Italia",
                    settings_name="Italia",
                    iso="IT",
                    fiscal_iso="IT",
                    uic="086",
                ),
                DetailedCountry(
                    name="Albania",
                    settings_name="Albania",
                    iso="AL",
                    fiscal_iso="AL",
                    uic="087",
                ),
            ]
        )
        expected_json = '{"data": [{"name": "Italia", "settings_name": "Italia", "iso": "IT", "fiscal_iso": "IT", "uic": "086"}, {"name": "Albania", "settings_name": "Albania", "iso": "AL", "fiscal_iso": "AL", "uic": "087"}]}'
        actual_json = json.dumps(model.to_dict(), default=json_serial)
        assert actual_json == expected_json


if __name__ == "__main__":
    unittest.main()
