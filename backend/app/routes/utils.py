import json
from flask import request, Response
from flask import Flask

Flask.make_response()
def get_context():
    """
    获取用户的open_id 和 http请求headers
    :return: open_id, data(json)
    """
    data = request.get_json()
    open_id = request.headers['x-wx-openid']
    return open_id, data


def make_response(status: int, msg: str, return_data: dict) -> Response:
    """
    标准请求返回
    :return: Response
    """
    return Response(json.dumps({"status": status, "msg": msg, "return_data": return_data}))

