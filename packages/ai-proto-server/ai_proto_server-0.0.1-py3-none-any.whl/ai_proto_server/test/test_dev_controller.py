# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from ai_proto_server.models.api_dev_gen_token_cap_get200_response import ApiDevGenTokenCapGet200Response  # noqa: E501
from ai_proto_server.models.api_dev_gen_token_post200_response import ApiDevGenTokenPost200Response  # noqa: E501
from ai_proto_server.models.api_dev_gen_token_post_request import ApiDevGenTokenPostRequest  # noqa: E501
from ai_proto_server.models.err_info import ErrInfo  # noqa: E501
from ai_proto_server.test import BaseTestCase


class TestDevController(BaseTestCase):
    """DevController integration test stubs"""

    def test_api_dev_gen_token_cap_get(self):
        """Test case for api_dev_gen_token_cap_get

        获取ai能力列表
        """
        headers = { 
            'Accept': 'application/json',
            'x_auth_token': 'x_auth_token_example',
        }
        response = self.client.open(
            '/api/dev/genToken/cap',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_dev_gen_token_post(self):
        """Test case for api_dev_gen_token_post

        生成authToken,只在开发模式下有效
        """
        api_dev_gen_token_post_request = ai_proto_server.ApiDevGenTokenPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/dev/genToken',
            method='POST',
            headers=headers,
            data=json.dumps(api_dev_gen_token_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
