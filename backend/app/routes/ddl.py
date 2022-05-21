import time

from flask import Blueprint
from routes.utils import get_context, check_data, make_response
from routes.rules.ddl_rules import *
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
    openid, data = get_context()
    check_data(AddDDLRules, data)

    # 数据库操作
    userid = User.query.filter(User.openid == openid).first().id
    new_ddl = Ddl(userid, data['title'], data['ddl_time'], int(time.time()*1000), data['content'], data.get('tag'),
                  data.get('course_uuid'), data.get('platform_uuid'))
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
                "create_time" -> int
                "tag" -> str(len 1 - 4096),
                "course_uuid" -> str
                "platform_uuid" -> str
                "is_completed" -> bool
            }
        ]
    }
    """
    openid, data = get_context()
    check_data(ListDDLsRules, data)

    if not 0 < data['end'] - data['start'] < 20:
        return make_response(400, "invalid range.(nmsl)", {})

    # 数据库操作
    userid = User.query.filter(User.openid == openid).first().id
    filter_list = [Ddl.userid == userid]
    if 'filter' in data:
        if data['filter']['is_completed']:
            filter_list.append(Ddl.is_completed is True)
        if data['filter']['is_overtime']:
            filter_list.append(Ddl.ddl_time < round(time.time() * 1000))
    if 'tag' in data:
        filter_list.append(Ddl.tag == data['tag'])
    return make_response(0, "OK", {'ddl_list': (Ddl.query.filter(*filter_list).
                                                order_by(Ddl.ddl_time.desc() if 'sorter' in data and data['sorter']['reversed']
                                                else Ddl.ddl_time).slice(data['start'], data['end']).all())})


@bp.route("/delete", methods=['POST', 'GET'])
def delete_ddl():
    """
    接受ddl删除请求，删除ddl
    :return: make_response()
    return_data = {"id" -> int(>=0)}
    """
    openid, data = get_context()
    check_data(DeleteDDLRules, data)

    # 数据库操作
    userid = User.query.filter(User.openid == openid).first().id
    del_ddl = Ddl.query.get(data['ddl_id'])
    if del_ddl is None:
        return make_response(404, "Ddl_id not found.(nmsl)", {})
    if del_ddl.userid != userid:
        return make_response(403, "Cannot delete others' ddl(nmsl).", {})

    db.session.delete(del_ddl)
    db.session.commit()

    return make_response(0, "OK", {"id": del_ddl.id})

