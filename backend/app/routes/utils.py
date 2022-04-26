import json
from flask import request


def get_context():
    """
    获取用户的open_id 和 http请求headers
    :return: open_id, data(json)
    """
    data = json.loads(request.get_data())
    open_id = request.headers['x-wx-openid']
    return open_id, data


def standard_response(status: int, msg: str, data: dict) -> dict:
    """
    标准请求返回
    :return: dict
    """
    return {"status": status, "msg": msg, "data": data}