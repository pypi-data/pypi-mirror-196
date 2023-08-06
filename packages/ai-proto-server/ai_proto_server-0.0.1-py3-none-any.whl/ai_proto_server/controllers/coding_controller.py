import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from ai_proto_server.models.api_coding_complete_lang_post_request import ApiCodingCompleteLangPostRequest  # noqa: E501
from ai_proto_server.models.api_coding_convert_lang_post_request import ApiCodingConvertLangPostRequest  # noqa: E501
from ai_proto_server.models.api_coding_explain_lang_post_request import ApiCodingExplainLangPostRequest  # noqa: E501
from ai_proto_server.models.api_coding_fix_error_lang_post_request import ApiCodingFixErrorLangPostRequest  # noqa: E501
from ai_proto_server.models.err_info import ErrInfo  # noqa: E501
from ai_proto_server import util


def api_coding_complete_lang_post(x_auth_token, lang, api_coding_complete_lang_post_request):  # noqa: E501
    """根据上下文补全代码

    根据上下文补全代码 # noqa: E501

    :param x_auth_token: 
    :type x_auth_token: str
    :param lang: 
    :type lang: str
    :param api_coding_complete_lang_post_request: 
    :type api_coding_complete_lang_post_request: dict | bytes

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        api_coding_complete_lang_post_request = ApiCodingCompleteLangPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_coding_convert_lang_post(x_auth_token, lang, api_coding_convert_lang_post_request):  # noqa: E501
    """对选中代码转换成其他编程语言

    对选中代码转换成其他编程语言 # noqa: E501

    :param x_auth_token: 
    :type x_auth_token: str
    :param lang: 
    :type lang: str
    :param api_coding_convert_lang_post_request: 
    :type api_coding_convert_lang_post_request: dict | bytes

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        api_coding_convert_lang_post_request = ApiCodingConvertLangPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_coding_explain_lang_post(x_auth_token, lang, api_coding_explain_lang_post_request):  # noqa: E501
    """解释选择代码

    解释选择代码 # noqa: E501

    :param x_auth_token: 
    :type x_auth_token: str
    :param lang: 
    :type lang: str
    :param api_coding_explain_lang_post_request: 
    :type api_coding_explain_lang_post_request: dict | bytes

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        api_coding_explain_lang_post_request = ApiCodingExplainLangPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_coding_fix_error_lang_post(x_auth_token, lang, api_coding_fix_error_lang_post_request):  # noqa: E501
    """根据错误提示给出解决方案

    根据错误提示给出解决方案 # noqa: E501

    :param x_auth_token: 
    :type x_auth_token: str
    :param lang: 
    :type lang: str
    :param api_coding_fix_error_lang_post_request: 
    :type api_coding_fix_error_lang_post_request: dict | bytes

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        api_coding_fix_error_lang_post_request = ApiCodingFixErrorLangPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_coding_gen_test_lang_post(x_auth_token, lang, api_coding_explain_lang_post_request):  # noqa: E501
    """对选中函数生成测试代码

    对选中函数生成测试代码 # noqa: E501

    :param x_auth_token: 
    :type x_auth_token: str
    :param lang: 
    :type lang: str
    :param api_coding_explain_lang_post_request: 
    :type api_coding_explain_lang_post_request: dict | bytes

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        api_coding_explain_lang_post_request = ApiCodingExplainLangPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
