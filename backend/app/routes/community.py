import json

from flask import Blueprint, jsonify
from routes.utils import get_context, check_data, make_response
from db.userSubs import UserSubscriptions
from db.sourceDdl import SourceDdl
from db.course import Course
from db.account import Account
from routes.utils import get_context_user, make_response


bp = Blueprint("community", __name__, url_prefix="/community")


@bp.route("/show_course", methods=["GET", "POST"])
def show_course():
    user, data = get_context_user(data_required=False)

    course_count = Course.query.count()
    courses = [i.to_dict() for i in Course.query.all()]
    for i in courses:
        i.update({"subscribed": True if i["course_uuid"] in map(lambda x: x.course_uuid, user.subscriptions.all()) else False})

    return make_response(0, "OK", {"courses": courses, "course_count": course_count})


@bp.route("/show_ddl", methods=["GET", "POST"])
def show_ddl():
    user, data = get_context_user(data_required=False)

    source_ddl_count = SourceDdl.query.count()
    source_ddls = [i.to_dict() for i in SourceDdl.query.all()]
    for i in source_ddls:
        i.update({"added": True if i["id"] in map(lambda x: x.source_ddl_id, user.ddls.all()) else False})

    return make_response(0, "OK", {"source_ddl_count": source_ddl_count, "source_ddls": source_ddls})


