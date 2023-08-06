import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from ai_proto_server.models.api_dev_gen_token_cap_get200_response import ApiDevGenTokenCapGet200Response  # noqa: E501
from ai_proto_server.models.api_dev_gen_token_post200_response import ApiDevGenTokenPost200Response  # noqa: E501
from ai_proto_server.models.api_dev_gen_token_post_request import ApiDevGenTokenPostRequest  # noqa: E501
from ai_proto_server.models.err_info import ErrInfo  # noqa: E501
from ai_proto_server import util


def api_dev_gen_token_cap_get(x_auth_token):  # noqa: E501
    """获取ai能力列表

    获取ai能力列表 # noqa: E501

    :param x_auth_token: 
    :type x_auth_token: str

    :rtype: Union[ApiDevGenTokenCapGet200Response, Tuple[ApiDevGenTokenCapGet200Response, int], Tuple[ApiDevGenTokenCapGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def api_dev_gen_token_post(api_dev_gen_token_post_request):  # noqa: E501
    """生成authToken,只在开发模式下有效

    生成authToken,只在开发模式下有效 # noqa: E501

    :param api_dev_gen_token_post_request: 
    :type api_dev_gen_token_post_request: dict | bytes

    :rtype: Union[ApiDevGenTokenPost200Response, Tuple[ApiDevGenTokenPost200Response, int], Tuple[ApiDevGenTokenPost200Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        api_dev_gen_token_post_request = ApiDevGenTokenPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
