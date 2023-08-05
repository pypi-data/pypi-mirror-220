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
from fattureincloud_python_sdk.models.company_info import CompanyInfo
from fattureincloud_python_sdk.models.company_type import CompanyType
from fattureincloud_python_sdk.models.company_info_access_info import (
    CompanyInfoAccessInfo,
)
from fattureincloud_python_sdk.models.company_info_plan_info import CompanyInfoPlanInfo
from fattureincloud_python_sdk.models.company_info_plan_info_functions import (
    CompanyInfoPlanInfoFunctions,
)
from fattureincloud_python_sdk.models.company_info_plan_info_functions_status import (
    CompanyInfoPlanInfoFunctionsStatus,
)
from fattureincloud_python_sdk.models.company_info_plan_info_limits import (
    CompanyInfoPlanInfoLimits,
)
from fattureincloud_python_sdk.models.function_status import FunctionStatus
from fattureincloud_python_sdk.models.permissions import Permissions
from fattureincloud_python_sdk.models.user_company_role import UserCompanyRole

globals()["CompanyInfo"] = CompanyInfo
from fattureincloud_python_sdk.models.get_company_info_response import (
    GetCompanyInfoResponse,
)


class TestGetCompanyInfoResponse(unittest.TestCase):
    """GetCompanyInfoResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetCompanyInfoResponse(self):
        """Test GetCompanyInfoResponse"""
        model = GetCompanyInfoResponse(
            data=CompanyInfo(
                id=1,
                name="mario",
                email="mariomail@gm.co",
                type=CompanyType("company"),
                accountant_id=10,
                is_accountant=True,
                access_info=CompanyInfoAccessInfo(
                    role=UserCompanyRole("master"),
                    permissions=Permissions(),
                    through_accountant=True,
                ),
                plan_info=CompanyInfoPlanInfo(
                    limits=CompanyInfoPlanInfoLimits(
                        clients=4000, suppliers=4000, products=4000, documents=4000
                    ),
                    functions=CompanyInfoPlanInfoFunctions(
                        archive=True, cerved=True, document_attachments=True
                    ),
                    functions_status=CompanyInfoPlanInfoFunctionsStatus(
                        ts_digital=FunctionStatus(active=True),
                        ts_pay=FunctionStatus(active=True),
                    ),
                ),
            )
        )
        expected_json = '{"data": {"id": 1, "name": "mario", "email": "mariomail@gm.co", "type": "company", "access_info": {"role": "master", "permissions": {}, "through_accountant": true}, "plan_info": {"limits": {"clients": 4000, "suppliers": 4000, "products": 4000, "documents": 4000}, "functions": {"archive": true, "cerved": true, "document_attachments": true}, "functions_status": {"ts_digital": {"active": true}, "ts_pay": {"active": true}}}, "accountant_id": 10, "is_accountant": true}}'
        actual_json = json.dumps(model.to_dict(), default=json_serial)
        assert actual_json == expected_json


if __name__ == "__main__":
    unittest.main()
