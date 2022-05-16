from flask import Blueprint

from crawler.util import list_crawlers
from routes.utils import get_context, make_response
import json

from db import db
from db.user import User

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/available", methods=['POST', 'GET'])
def available_account_type():
    tmp = []
    for c in list_crawlers():
        tmp.append({"name": c['name'], "uuid": c['uuid'], "fields": c['obj'].required_fields()})
    return make_response(0, "OK", tmp)


@bp.route("/add", methods=['POST', 'GET'])
def add_account():
    data, open_id = get_context()

    return make_response(0, "OK", {})


@bp.route("/list", methods=['POST', 'GET'])
def list_account():
    data, open_id = get_context()

    return


@bp.route("/delete", methods=['POST', 'GET'])
def delete_account():
    data, open_id = get_context()

    return

