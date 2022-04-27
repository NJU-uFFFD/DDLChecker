import json
from flask import request, abort, jsonify, Response
from marshmallow import Schema, fields, ValidationError





def get_context():
    """
    获取用户的open_id 和 http请求headers
    :return: open_id, data(json)
    """
    data = jsonify(request.get_data())
    open_id = request.headers['x-wx-openid']
    return open_id, data


def make_response(status: int, msg: str, data: dict) -> Response:
    """
    标准请求返回
    :return: Response
    """
    return Response(json.dumps({"status": status, "msg": msg, "data": data}))
