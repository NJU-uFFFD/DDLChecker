from flask import Blueprint
from routes.utils import get_context, make_response
import json

bp = Blueprint("account", __name__, url_prefix="/account")


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
