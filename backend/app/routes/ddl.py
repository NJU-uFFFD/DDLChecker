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
    user = User.query.filter(User.openid == openid).first()
    if user is None:
        return make_response(-1, "User not registered", {})
    userid = user.id
    new_ddl = Ddl(userid, data['title'], data['ddl_time'], int(time.time() * 1000), data['content'], data.get('tag'),
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
                "is_deleted" -> bool
                "complete_time" -> int
                "delete_time" -> int
            }
        ]
        "ddl_count" -> int
    }
    """
    openid, data = get_context()
    check_data(ListDDLsRules, data)

    if not 0 <= data['end'] - data['start'] <= 20:
        return make_response(400, "Invalid slice range.(nmsl)", {})

    # 数据库操作
    user = User.query.filter(User.openid == openid).first()
    if user is None:
        return make_response(-1, "User not registered.", {})
    userid = user.id
    filter_list = [Ddl.userid == userid]
    if 'filter' in data:
        if 'is_not_completed' in data['filter'] and data['filter']['is_not_completed']:
                filter_list.append(Ddl.is_completed == False)
        if 'is_completed' in data['filter'] and data['filter']['is_completed']:
                filter_list.append(Ddl.is_completed == True)
        if 'is_not_overtime' in data['filter']and data['filter']['is_not_overtime']:
                filter_list.append(Ddl.ddl_time >= round(time.time() * 1000))
        if 'is_overtime' in data['filter']and data['filter']['is_overtime']:
                filter_list.append(Ddl.ddl_time < round(time.time() * 1000))
        filter_list.append(Ddl.is_deleted == False)
        if 'is_deleted' in data['filter']:
            if data['filter']['is_deleted']:
                filter_list.append(Ddl.is_deleted == True)
    if 'tag' in data:
        filter_list.append(Ddl.tag == data['tag'])
    if 'time_range' in data:
        if 'start' in data['time_range'] and 'end' in data['time_range']:
            if data['time_range']['start'] > data['time_range']['end']:
                return make_response(400, "Invalid time range.(nmsl)", {})
            else:
                filter_list.append(data['time_range']['start'] <= Ddl.ddl_time)
                filter_list.append(data['time_range']['end'] >= Ddl.ddl_time)
    ddl_count = len(
        Ddl.query.filter(*filter_list).order_by(Ddl.ddl_time.desc() if 'sorter' in data and 'reversed' in data['sorter'] and data['sorter']['reversed']
                                                else Ddl.ddl_time).all())
    return make_response(0, "OK", {'ddl_list': (Ddl.query.filter(*filter_list).
                                                order_by(
        Ddl.ddl_time.desc() if 'sorter' in data and 'reversed' in data['sorter'] and data['sorter']['reversed']
        else Ddl.ddl_time).slice(data['start'], data['end']).all()),
                                   'ddl_count': ddl_count})


@bp.route("/update", methods=['POST', 'GET'])
def update_ddl():
    """
    接受ddl更新请求，更新ddl
    :return: make_response()
    return_data = {"id" -> int(>=0)}
    """
    openid, data = get_context()
    check_data(UpdateDDLRules, data)

    # 数据库操作
    user = User.query.filter(User.openid == openid).first()
    if user is None:
        return make_response(-1, "User not registered", {})
    userid = user.id
    ddl = Ddl.query.get(data['id'])
    if ddl is None:
        return make_response(404, "Id not found.(nmsl)", {})
    if ddl.userid != userid:
        return make_response(403, "Cannot delete others' ddl(nmsl).", {})

    if 'title' in data:
        ddl.title = data['title']
    if 'content' in data:
        ddl.content = data['content']
    if 'ddl_time' in data:
        ddl.ddl_time = data['ddl_time']
    if 'tag' in data:
        ddl.tag = data['tag']
    if 'course_uuid' in data:
        ddl.course_uuid = data['course_uuid']
    if 'platform_uuid' in data:
        ddl.platform_uuid = data['platform_uuid']
    if 'is_completed' in data:
        ddl.is_completed = data['is_completed']
        if data['is_completed']:
            ddl.complete_time = round(time.time() * 1000)
        else:
            ddl.complete_time = None
    if 'is_deleted' in data:
        ddl.is_deleted = data['is_deleted']
        if data['is_deleted']:
            ddl.delete_time = round(time.time() * 1000)
        else:
            ddl.delete_time = None
    db.session.commit()

    return make_response(0, "OK", {"id": ddl.id})
