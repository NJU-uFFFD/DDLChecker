import json
import time
import uuid


from flask import Blueprint

from db import db
from routes.rules.community_rules import AddCourseRulesForCommunity, AddDDLRulesForCommunity, SubscribeCourseRules, \
    FetchDDLRuleForCommunity, ListCourseRulesForCommunity, ListDDLRulesForCommunity, DeleteDDlRuleForCommunity, \
    DeleteCourseRuleForCommunity
from routes.rules.ddl_rules import ListDDLsRules
from routes.utils import get_context, check_data, make_response
from db.userSubs import UserSubscriptions
from db.ddl import Ddl
from db.sourceDdl import SourceDdl
from db.course import Course
from db.account import Account
from routes.utils import get_context_user, make_response

bp = Blueprint("community", __name__, url_prefix="/community")


@bp.route("/course/list", methods=["GET", "POST"])
def list_course():
    user, data = get_context_user()
    check_data(ListCourseRulesForCommunity, data)

    subs = list(map(lambda x: x.course_uuid, user.subscriptions.all()))

    filter_list = []
    if "key_word" in data:
        filter_list.append(Course.course_name.contains(data["key_word"]))

    if "filter" in data:
        if "is_subscribed" in data["filter"] and data['filter']['is_subscribed']:
            filter_list.append(Course.course_uuid.in_(subs))

    if "platform_uuids" in data:
        for platform_uuid in data["platform_uuids"]:
            # 反向传值
            filter_list.append(Course.platform_uuid != platform_uuid)

    page = Course.query.filter(*filter_list).paginate(data["page"], data["size"])
    course_count = page.total
    total_pages = page.pages
    courses = [i.to_dict() for i in page.items]

    for i in courses:
        i.update({"subscribed": i["course_uuid"] in subs})

    return make_response(0, "OK", {"courses": courses, "course_count": course_count, "total_pages": total_pages})


@bp.route("/ddl/list", methods=["GET", "POST"])
def list_ddl():
    user, data = get_context_user()
    check_data(ListDDLRulesForCommunity, data)

    page = SourceDdl.query.filter(SourceDdl.course_uuid == data['course_uuid']).order_by(SourceDdl.ddl_time.desc()).paginate(data["page"], data["size"])
    source_ddl_count = page.total
    total_pages = page.pages
    source_ddls = [i.to_dict() for i in page.items]
    src = list(map(lambda x: x.source_ddl_id, user.ddls.filter(Ddl.source_ddl_id != None).all()))
    for i in source_ddls:
        i.update({"added": i["id"] in src})
        i.update({"self": i["creator_id"] == user.id})

    return make_response(0, "OK", {"source_ddl_count": source_ddl_count, "source_ddls": source_ddls, "total_pages": total_pages})


@bp.route("/course/add", methods=["GET", "POST"])
def add_course():
    user, data = get_context_user()
    check_data(AddCourseRulesForCommunity, data)

    if Course.query.filter(
            Course.course_uuid == str(uuid.uuid5(uuid.UUID(data["platform_uuid"]), data["course_name"]))).count() != 0:
        return make_response(-1, "Course already exists, change another name.(nmsl)", {}, 400)

    course = Course(data["course_name"], str(uuid.uuid5(uuid.UUID(data["platform_uuid"]), data["course_name"])),
                    data["platform_uuid"], creator_id=user.id)

    db.session.add(course)
    sub = UserSubscriptions(user.id, course.course_uuid, data["platform_uuid"])
    db.session.add(sub)
    db.session.commit()

    return make_response(0, "OK", {"course_uuid": course.course_uuid})


@bp.route("/ddl/add", methods=["GET", "POST"])
def add_ddl():
    user, data = get_context_user()
    check_data(AddDDLRulesForCommunity, data)

    if Course.query.filter(Course.course_uuid == data["course_uuid"]).first() is None:
        return make_response(-1, "Course not found.(nmsl)", {})

    if SourceDdl.query.filter(SourceDdl.title == data['title'], SourceDdl.ddl_time == data['ddl_time']).count() >= 1:
        return make_response(-1, "Ddl already existed! (nmsl)", {})

    ddl = SourceDdl(data["course_uuid"], Course.query.get(data["course_uuid"]).platform_uuid, data["title"], data["content"], "",
                    data["ddl_time"], time.time() * 1000, creator_id=user.id)
    db.session.add(ddl)

    db.session.commit()

    return make_response(0, "OK", {"id": ddl.id})


@bp.route("/course/subscribe", methods=["GET", "POST"])
def subscribe_course():
    user, data = get_context_user()
    check_data(SubscribeCourseRules, data)

    course = Course.query.filter(Course.course_uuid == data["course_uuid"]).first()
    if course is None:
        return make_response(-1, "Course not exists(nmsl).", {}, 400)

    sub = UserSubscriptions(user.id, data["course_uuid"], course.platform_uuid)

    if user.subscriptions.filter(UserSubscriptions.course_uuid == data['course_uuid']).first() is not None:
        return make_response(-1, "Subscription already exists.(nmsl)", {}, 400)

    now_time = int(time.time() * 1000)

    for ddl in SourceDdl.query.filter(SourceDdl.course_uuid == sub.course_uuid, SourceDdl.creator_id == None).all():
        if ddl.ddl_time > now_time:
            to_add = Ddl(sub.userid, ddl.title, ddl.ddl_time, ddl.create_time, ddl.content, "",
                                 sub.course_uuid, sub.platform_uuid, ddl.id)
            db.session.add(to_add)

    sub.last_updated = now_time

    db.session.add(sub)
    db.session.commit()

    return make_response(0, "OK", {"id": sub.id})


@bp.route("/course/unsubscribe", methods=["GET", "POST"])
def unsubscribe_course():
    user, data = get_context_user()
    check_data(SubscribeCourseRules, data)

    sub = user.subscriptions.filter(UserSubscriptions.course_uuid == data['course_uuid'],
                                    UserSubscriptions.userid == user.id).first()
    if sub is None:
        return make_response(-1, "Subscription not exists.(What's wrong with you?)(nmsl)", {}, 400)

    db.session.delete(sub)
    db.session.commit()

    return make_response(0, "OK", {"id": sub.id})


@bp.route("/ddl/fetch", methods=["GET", "POST"])
def fetch_ddl():
    user, data = get_context_user()
    check_data(FetchDDLRuleForCommunity, data)

    source_ddl = SourceDdl.query.get(data['id'])

    if source_ddl is None:
        return make_response(-1, "SourceDdl not exists.(nmsl)", {})

    if user.ddls.filter(Ddl.source_ddl_id == data['id']).first() is not None:
        return make_response(-1, "SourceDdl already added.(nmsl)", {})

    ddl = Ddl(user.id, source_ddl.title, source_ddl.ddl_time, int(time.time() * 1000), source_ddl.content,
              source_ddl.tag, source_ddl.course_uuid, source_ddl.platform_uuid, source_ddl.id)

    db.session.add(ddl)
    db.session.commit()

    return make_response(0, "OK", {"id": ddl.id})


@bp.route("/ddl/delete", methods=["GET", "POST"])
def delete_ddl():
    user, data = get_context_user()
    check_data(DeleteDDlRuleForCommunity, data)

    source_ddl = SourceDdl.query.get(data["id"])

    if source_ddl is None:
        return make_response(-1, "Ddl not found.(nmsl)", {})

    if source_ddl.creator_id != user.id:
        return make_response(-1, "Can only delete ddls created by your own", {})

    db.session.delete(source_ddl)

    db.session.commit()
    return make_response(0, "OK", {"id": source_ddl.id})


@bp.route("/course/delete", methods=["GET", "POST"])
def delete_course():
    user, data = get_context_user()
    check_data(DeleteCourseRuleForCommunity, data)

    course = Course.query.get(data["course_uuid"])

    if course is None:
        return make_response(-1, "Course not found.(nmsl)", {})

    if course.creator_id != user.id:
        return make_response(-1, "Can only delete courses created by your own.", {})

    if course.source_ddls.count() > 0:
        return make_response(-1, "Others have already created ddls in the course you created.", {})

    if course.subscriptions.filter(UserSubscriptions.userid != user.id).count() > 0:
        return make_response(-1, "Other have already subscribed the course created by you.", {})

    user_sub = user.subscriptions.filter(UserSubscriptions.course_uuid == course.course_uuid).first()

    if user_sub is not None:
        db.session.delete(user_sub)

    db.session.delete(course)

    db.session.commit()
    return make_response(0, "OK", {"id": course.course_uuid})





