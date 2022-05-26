from flask import Blueprint

from crawler.util import list_crawlers
from routes.utils import get_context_user, make_response, check_data
from routes.rules.account_rules import *
from db.account import Account
from db import db

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/available", methods=['POST', 'GET'])
def available_account_type():
    user, data = get_context_user(data_required=False)
    current_accounts = user.accounts.all()
    tmp = []
    for c in list_crawlers():
        bound = True in [c['uuid'] == account.platform_uuid for account in current_accounts]
        tmp.append({"name": c['name'], "platform_uuid": c['uuid'], "fields": c['obj'].required_fields(), "bound": bound})
    return make_response(0, "OK", {"available_account_type": tmp})


@bp.route("/add", methods=['POST', 'GET'])
def add_account():
    user, data = get_context_user()
    check_data(AddAccountRules, data)
    # 检查 account 是否存在
    if user.accounts.filter(Account.platform_uuid == data['platform_uuid']).all():
        return make_response(-1, "Cannot add more than one account for each platform", {})
    new_account = Account(user.id, data['platform_uuid'], data['fields'])
    db.session.add(new_account)
    db.session.commit()

    return make_response(0, "OK", {"id": new_account.id})


@bp.route("/list", methods=['POST', 'GET'])
def list_account():
    user, data = get_context_user()

    return


@bp.route("/update", methods=['POST', 'GET'])
def update_account():
    user, data = get_context_user()
    check_data(UpdateAccountRules, data)

    account = Account.query.get(data['id'])
    if account is None:
        return make_response(404, "Id not found(nmsl)", {})
    if account.userid != user.id:
        return make_response(403, "Cannot delete others' account(nmsl).", {})

    if 'fields' in data:
        account.fields = data['fields']

    if 'delete_account' in data and data['delete_account'] is True:
        db.session.delete(account)

    db.session.commit()

    return make_response(0, "OK", {"id": account.id})



