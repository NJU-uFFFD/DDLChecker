import json
import time
import uuid

from flask import Blueprint, jsonify

from db import db
from routes.rules.community_rules import AddCourseRulesForCommunity, AddDDLRulesForCommunity
from routes.utils import get_context, check_data, make_response
from db.userSubs import UserSubscriptions
from db.sourceDdl import SourceDdl
from db.course import Course
from db.account import Account
from routes.utils import get_context_user, make_response


bp = Blueprint("community", __name__, url_prefix="/community")


@bp.route("/course/list", methods=["GET", "POST"])
def list_course():
    user, data = get_context_user(data_required=False)

    course_count = Course.query.count()
    courses = [i.to_dict() for i in Course.query.all()]
    for i in courses:
        i.update({"subscribed": True if i["course_uuid"] in map(lambda x: x.course_uuid, user.subscriptions.all()) else False})

    return make_response(0, "OK", {"courses": courses, "course_count": course_count})


@bp.route("/ddl/list", methods=["GET", "POST"])
def list_ddl():
    user, data = get_context_user(data_required=False)

    source_ddl_count = SourceDdl.query.count()
    source_ddls = [i.to_dict() for i in SourceDdl.query.all()]
    for i in source_ddls:
        i.update({"added": True if i["id"] in map(lambda x: x.source_ddl_id, user.ddls.all()) else False})

    return make_response(0, "OK", {"source_ddl_count": source_ddl_count, "source_ddls": source_ddls})


@bp.route("/course/add", methods=["GET", "POST"])
def add_course():
    user, data = get_context_user()
    check_data(AddCourseRulesForCommunity, data)

    course = Course(data["course_name"], str(uuid.uuid3(uuid.UUID(data["platform_uuid"]), data["course_name"])), data["platform_uuid"], creator_id=user.id)

    db.session.add(course)
    sub = UserSubscriptions(user.id, data["course_uuid"], data["platform_uuid"])
    db.session.add(sub)
    db.session.commit()

    return make_response(0, "OK", {"course_uuid": course.course_uuid})


@bp.route("/ddl/add", methods=["GET", "POST"])
def add_ddl():
    user, data = get_context_user()
    check_data(AddDDLRulesForCommunity, data)

    ddl = SourceDdl(data["course_uuid"], data["platform_uuid"], data["title"], data["content"], data["tag"], data["ddl_time"], time.time() * 1000, creator_id=user.id)
    db.session.add(ddl)

    db.session.commit()

    return make_response(0, "OK", {"id": ddl.id})




