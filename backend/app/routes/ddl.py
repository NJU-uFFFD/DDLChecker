from flask import Blueprint
from routes.utils import get_context, make_response
from routes.rules import *


bp = Blueprint("ddl", __name__, url_prefix="/ddl")


@bp.route("/add", methods=['POST', 'GET'])
def add_ddl():
    """
    接受手动添加ddl请求，添加ddl：
    :return: make_response()
    return_data = { "ddl_id" -> int(>=0) }
    """
    open_id, data = get_context()
    check_data(AddDDLRules, data)

    # 数据库操作

    return make_response(0, "OK", {})


@bp.route("/list", methods=['POST', 'GET'])
def list_dll():
    """
    接受ddl查询请求，返回用户查询的ddl(默认按照时间顺序排序， filter可选)
    :return: make_response()
    return_data = {
        "ddl_list" ->list[{
                "ddl_id" ->int(>=0),
                "title" -> str (len 1 - 128),
                "content" -> str (len 1 - 256)(not necessary),
                "ddl_time" -> int(不得在30天前),
                "tag" -> str(not necessary),
                "course_uuid" -> uuid(not necessary)
            }
        ]
    }
    """
    open_id, data = get_context()
    check_data(ListDDLsRules, data)

    # 数据库操作

    return make_response(0, "OK", {})


@bp.route("/delete", methods=['POST', 'GET'])
def delete_ddl():
    """
    接受ddl删除请求，删除ddl
    :return: make_response()
    return_data = { "ddl_id" -> int(>=0) }
    """
    open_id, data = get_context()
    check_data(DeleteDDLRules, data)

    # 数据库操作

    return make_response(0, "OK", {})

