# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from ai_proto_server.models.api_coding_complete_lang_post_request import ApiCodingCompleteLangPostRequest  # noqa: E501
from ai_proto_server.models.api_coding_convert_lang_post_request import ApiCodingConvertLangPostRequest  # noqa: E501
from ai_proto_server.models.api_coding_explain_lang_post_request import ApiCodingExplainLangPostRequest  # noqa: E501
from ai_proto_server.models.api_coding_fix_error_lang_post_request import ApiCodingFixErrorLangPostRequest  # noqa: E501
from ai_proto_server.models.err_info import ErrInfo  # noqa: E501
from ai_proto_server.test import BaseTestCase


class TestCodingController(BaseTestCase):
    """CodingController integration test stubs"""

    def test_api_coding_complete_lang_post(self):
        """Test case for api_coding_complete_lang_post

        根据上下文补全代码
        """
        api_coding_complete_lang_post_request = ai_proto_server.ApiCodingCompleteLangPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x_auth_token': 'x_auth_token_example',
        }
        response = self.client.open(
            '/api/coding/complete/{lang}'.format(lang='lang_example'),
            method='POST',
            headers=headers,
            data=json.dumps(api_coding_complete_lang_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_coding_convert_lang_post(self):
        """Test case for api_coding_convert_lang_post

        对选中代码转换成其他编程语言
        """
        api_coding_convert_lang_post_request = ai_proto_server.ApiCodingConvertLangPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x_auth_token': 'x_auth_token_example',
        }
        response = self.client.open(
            '/api/coding/convert/{lang}'.format(lang='lang_example'),
            method='POST',
            headers=headers,
            data=json.dumps(api_coding_convert_lang_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_coding_explain_lang_post(self):
        """Test case for api_coding_explain_lang_post

        解释选择代码
        """
        api_coding_explain_lang_post_request = ai_proto_server.ApiCodingExplainLangPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x_auth_token': 'x_auth_token_example',
        }
        response = self.client.open(
            '/api/coding/explain/{lang}'.format(lang='lang_example'),
            method='POST',
            headers=headers,
            data=json.dumps(api_coding_explain_lang_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_coding_fix_error_lang_post(self):
        """Test case for api_coding_fix_error_lang_post

        根据错误提示给出解决方案
        """
        api_coding_fix_error_lang_post_request = ai_proto_server.ApiCodingFixErrorLangPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x_auth_token': 'x_auth_token_example',
        }
        response = self.client.open(
            '/api/coding/fixError/{lang}'.format(lang='lang_example'),
            method='POST',
            headers=headers,
            data=json.dumps(api_coding_fix_error_lang_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_coding_gen_test_lang_post(self):
        """Test case for api_coding_gen_test_lang_post

        对选中函数生成测试代码
        """
        api_coding_explain_lang_post_request = ai_proto_server.ApiCodingExplainLangPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x_auth_token': 'x_auth_token_example',
        }
        response = self.client.open(
            '/api/coding/genTest/{lang}'.format(lang='lang_example'),
            method='POST',
            headers=headers,
            data=json.dumps(api_coding_explain_lang_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
