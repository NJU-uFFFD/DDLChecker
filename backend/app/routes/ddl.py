from flask import Blueprint
from routes.utils import get_context, make_response
from routes.rules import *


bp = Blueprint("ddl", __name__, url_prefix="/ddl")


@bp.route("/add", methods=['POST', 'GET'])
def add_ddl():
    """
    允许用户手动添加ddl
    data:   "title" -> str (len 1 - 128)
            "content" -> str (len 1 - 256)
            "ddl_time" -> int
            "tag" -> str
            "course_uuid" -> uuid
    :return: standard_response()
    """
    # open_id, data = get_context()

    json = {"title": "s"}
    data = check_data(AddDDLRules, json)

    return make_response(0, "OK", {})


@bp.route("/list", methods=['POST', 'GET'])
def list_dll():
    open_id, data = get_context()

    return make_response(0, "OK", {})


@bp.route("/delete", methods=['POST', 'GET'])
def delete_ddl():
    open_id, data = get_context()

    return make_response(0, "OK", {})

