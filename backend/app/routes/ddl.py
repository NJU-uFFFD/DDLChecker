from flask import Blueprint
from routes.utils import get_context_user, check_data, make_response
from routes.rules.ddl_rules import *
from db import db
from db.ddl import Ddl
from db.course import Course
from db.user import User

bp = Blueprint("ddl", __name__, url_prefix="/ddl")


@bp.route("/add", methods=['POST', 'GET'])
def add_ddl():
    """
    接受手动添加ddl请求，添加ddl：
    :return: make_response()
    return_data = {"id" -> int(>=0)}
    """
    user, data = get_context_user()
    check_data(AddDDLRules, data)

    if 'course_uuid' in data and Course.query.get(data['course_uuid']) is None:
        return make_response(-1, "Course does not exist", {})

    new_ddl = Ddl(user.id, data['title'], data['ddl_time'], int(time.time() * 1000), data['content'], data.get('tag'),
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
    user, data = get_context_user()
    check_data(ListDDLsRules, data)

    filter_list = []
    if 'filter' in data:
        if 'is_completed' in data['filter']:
            if data['filter']['is_completed']:
                filter_list.append(Ddl.is_completed == True)
            else:
                filter_list.append(Ddl.is_completed == False)
        if 'is_overtime' in data['filter']:
            if data['filter']['is_overtime']:
                filter_list.append(Ddl.ddl_time < round(time.time() * 1000))
            else:
                filter_list.append(Ddl.ddl_time >= round(time.time() * 1000))
        if 'is_deleted' in data['filter']:
            if data['filter']['is_deleted']:
                filter_list.append(Ddl.is_deleted == True)
            else:
                filter_list.append(Ddl.is_deleted == False)
    if 'tag' in data:
        filter_list.append(Ddl.tag == data['tag'])
    if 'ddl_time_range' in data:
        if 'start' in data['ddl_time_range'] and 'end' in data['ddl_time_range']:
            if data['ddl_time_range']['start'] > data['ddl_time_range']['end']:
                return make_response(400, "Invalid time range.(nmsl)", {})
            else:
                filter_list.append(data['ddl_time_range']['start'] <= Ddl.ddl_time)
                filter_list.append(data['ddl_time_range']['end'] >= Ddl.ddl_time)
        else:
            return make_response(-1, "missing start or end.", {})
    if 'create_time_range' in data:
        if 'start' in data['create_time_range'] and 'end' in data['create_time_range']:
            if data['create_time_range']['start'] > data['create_time_range']['end']:
                return make_response(400, "Invalid time range.(nmsl)", {})
            else:
                filter_list.append(data['create_time_range']['start'] <= Ddl.create_time)
                filter_list.append(data['create_time_range']['end'] >= Ddl.create_time)
        else:
            return make_response(-1, "missing start or end.", {})
    if 'complete_time_range' in data:
        if 'start' in data['complete_time_range'] and 'end' in data['complete_time_range']:
            if data['complete_time_range']['start'] > data['complete_time_range']['end']:
                return make_response(400, "Invalid time range.(nmsl)", {})
            else:
                filter_list.append(data['complete_time_range']['start'] <= Ddl.complete_time)
                filter_list.append(data['complete_time_range']['end'] >= Ddl.complete_time)
        else:
            return make_response(-1, "missing start or end.", {})

    page = user.ddls.filter(*filter_list).order_by(Ddl.ddl_time.desc() if 'sorter' in data and 'reversed' in data['sorter'] and data['sorter']['reversed']
                                                else Ddl.ddl_time).paginate(data['page'], data['size'])

    ddl_count = page.total
    total_pages = page.pages
    return make_response(0, "OK", {'ddl_list': page.items, 'ddl_count': ddl_count, "total_pages": total_pages})


@bp.route("/update", methods=['POST', 'GET'])
def update_ddl():
    """
    接受ddl更新请求，更新ddl
    :return: make_response()
    return_data = {"id" -> int(>=0)}
    """
    user, data = get_context_user()
    check_data(UpdateDDLRules, data)

    # 数据库操作
    ddl = Ddl.query.get(data['id'])
    if ddl is None:
        return make_response(404, "Id not found.(nmsl)", {})
    if ddl.userid != user.id:
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
