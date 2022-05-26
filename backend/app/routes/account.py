from flask import Blueprint

from crawler.util import list_crawlers
from routes.utils import get_context_user, make_response
from db.account import Account

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/available", methods=['POST', 'GET'])
def available_account_type():
    user, data = get_context_user(data_required=False)
    current_accounts = user.accounts.all()
    tmp = []
    for c in list_crawlers():
        bound = True in [c['uuid'] == account.platform_uuid for account in current_accounts]
        tmp.append({"name": c['name'], "uuid": c['uuid'], "fields": c['obj'].required_fields(), "bound": bound})
    return make_response(0, "OK", {"available_account_type": tmp})


@bp.route("/add", methods=['POST', 'GET'])
def add_account():
    user, data = get_context_user()

    # 检查 account 是否存在

    return make_response(0, "OK", {})


@bp.route("/list", methods=['POST', 'GET'])
def list_account():
    user, data = get_context_user()

    return


@bp.route("/delete", methods=['POST', 'GET'])
def delete_account():
    user, data = get_context_user()

    return

