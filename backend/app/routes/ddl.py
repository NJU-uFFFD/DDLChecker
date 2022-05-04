from flask import Blueprint, jsonify
from routes.utils import get_context, make_response
from routes.rules import *
from db import db
from db.ddl import Ddl
from db.user import User


bp = Blueprint("ddl", __name__, url_prefix="/ddl")


@bp.route("/add", methods=['POST', 'GET'])
def add_ddl():
    """
    接受手动添加ddl请求，添加ddl：
    :return: make_response()
    return_data = {"id" -> int(>=0)}
    """
    open_id, data = get_context()
    check_data(AddDDLRules, data)

    # 数据库操作
    userid = User.query.filter(User.openid == open_id).first().id
    new_ddl = Ddl(userid, data['title'], data['ddl_time'], data['content'], data['tag'], data['course_uuid'])
    db.session.add(new_ddl)
    db.session.commit()

    return make_response(0, "OK", {'id': new_ddl.id})


@bp.route("/list", methods=['POST', 'GET'])
def list_dll():
    """
    接受ddl查询请求，返回用户查询的ddl(默认按照时间顺序排序， filter可选)
    :return: make_response()
    return_data = {
        "ddl_list" ->list[{
                "userid" -> int(>=0)
                "id" ->int(>=0),
                "title" -> str (len 1 - 256),
                "content" -> str (len 1 - 4096),
                "ddl_time" -> int(不得在30天前),
                "tag" -> str(len 1 - 4096),
                "course_uuid" -> uuid
                "is_completed" -> bool
            }
        ]
    }
    """
    open_id, data = get_context()
    check_data(ListDDLsRules, data)

    # 数据库操作
    userid = User.query.filter(User.openid == open_id).first().id
    filter_list = [Ddl.userid == userid]
    if data['filter']['is_completed']:
        filter_list.append(Ddl.is_completed is True)
    if data['filter']['is_overtime']:
        filter_list.append(Ddl.ddl_time > round(time.time() * 1000))
    return make_response(0, "OK", {'ddl_list': (Ddl.query.filter(*filter_list).all())})


@bp.route("/delete", methods=['POST', 'GET'])
def delete_ddl():
    """
    接受ddl删除请求，删除ddl
    :return: make_response()
    return_data = {"id" -> int(>=0)}
    """
    open_id, data = get_context()
    check_data(DeleteDDLRules, data)

    # 数据库操作
    userid = User.query.filter(User.openid == open_id).first().id
    del_ddl = Ddl.query.get(data['ddl_id'])
    # if del_ddl is None:
    #     return make_response(-1, "ddl_id not found", {})

    db.session.delete(del_ddl)
    db.session.commit()

    return make_response(0, "OK", {"id": del_ddl.id})

