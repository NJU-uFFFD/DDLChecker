from flask import Blueprint
from routes.utils import get_context, make_response
from routes.rules import *


bp = Blueprint("ddl", __name__, url_prefix="/ddl")


@bp.route("/add", methods=['POST', 'GET'])
def add_ddl():
    """
    用户手动添加ddl
    :return: make_response()
    """
    open_id, data = get_context()
    check_data(AddDDLRules, data)

    return make_response(0, "OK", {})


@bp.route("/list", methods=['POST', 'GET'])
def list_dll():
    """
    返回用户查询的ddl(默认按照时间顺序排序， filter可选)
    :return: make_response()
    """
    open_id, data = get_context()
    check_data(ListDDLsRules, data)

    return make_response(0, "OK", {})


@bp.route("/delete", methods=['POST', 'GET'])
def delete_ddl():
    open_id, data = get_context()

    return make_response(0, "OK", {})

