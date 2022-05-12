from flask import request, Response, jsonify
from flask import abort
from marshmallow import ValidationError


def get_context():
    """
    获取用户的 open_id 和 http 请求 headers
    :return: open_id, data(json)
    """
    data = request.get_json()
    openid = request.headers['x-wx-openid']
    return openid, data


def make_response(status: int, msg: str, return_data: dict) -> Response:
    """
    标准请求返回
    :return: Response
    """
    return jsonify({"code": status, "msg": msg, "data": return_data})


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
        abort(make_response(status=-1, msg=str(e.messages), return_data={}), 400)
