import json
import logging

import requests
from flask import abort
from flask import request, Response, jsonify
from marshmallow import ValidationError
from util.sensitive_words_blocking.words_blocking import DFA

from db.user import User


def get_context(data_required=True):
    """
    获取用户的 open_id 和 http 请求内容
    :return: open_id, data(json)
    """
    if data_required:
        data = request.get_data().decode('utf-8')
        # 屏蔽词检查
        dfa = DFA()
        data = dfa.filter_all(data)
        print(data)
        data = json.loads(data)

    else:
        data = None

    openid = None
    # 启用公网访问后防止用户伪造 openid
    if 'x-wx-source' in request.headers:
        openid = request.headers['x-wx-openid']

    return openid, data


def get_context_user(data_required=True):
    """
    获取 user 和 http 请求内容
    :return: user, data(json)
    """
    openid, data = get_context(data_required)
    user = User.query.filter(User.openid == openid).first()

    if not user:
        abort(make_response(status=-1, msg="Unauthorized or not registered.", return_data={}), 403)

    return user, data


def make_response(status: int, msg: str, return_data: dict, http_status_code=200) -> Response:
    """
    标准请求返回
    :return: Response
    """
    ret = jsonify({"code": status, "msg": msg, "data": return_data})
    ret.status_code = http_status_code
    return ret


def check_data(schema, data):
    """
    json输入格式校验
    :param schema: 校验规则
    :param data: 校验数据
    :return:若校验失败，abort并返回错误
    """
    try:
        return schema().load(data)
    except ValidationError as e:
        abort(make_response(status=-1, msg=str(e.messages), return_data={}, http_status_code=400))


