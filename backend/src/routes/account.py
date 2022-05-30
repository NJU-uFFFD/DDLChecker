import json
import logging

from flask import Blueprint
from crawler.util import list_crawlers
from routes.utils import get_context_user, make_response, check_data
from routes.rules.account_rules import *
from db.account import Account
from db.course import Course
from db.userSubs import UserSubscriptions
from db import db
from util.encrypt import aes_encrypt

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
    """
    添加账户
    :return: make_response(
    return data = {"id" -> int}
    """
    user, data = get_context_user()
    check_data(AddAccountRules, data)

    user.account_add_times += 1
    db.session.commit()

    if user.account_add_times >= 30:
        return make_response(-1, "Reaching add account times limitation", {})

    # 检查 account 是否存在
    if user.accounts.filter(Account.platform_uuid == data['platform_uuid']).all():
        return make_response(-1, "Cannot add more than one account for each platform", {})
    account = Account(user.id, data['platform_uuid'], aes_encrypt(json.dumps(data['fields'])))

    crawler_obj = None
    check_required = False
    for i in list_crawlers():
        if i['uuid'] == account.platform_uuid:
            crawler_obj = i['obj']
            check_required = i['check']
    if crawler_obj is None:
        return make_response(-1, "Invalid platform_uuid", {})
    crawler = crawler_obj()

    if check_required:
        try:
            crawler.login(data['fields'])
            courses = crawler.fetch_course()
            logging.info(courses)
            account.status = "已验证, 待爬取"
        except Exception as e:
            logging.exception(e)
            return make_response(-1, str(e), {})

        for c in courses:
            if not Course.query.filter(Course.course_uuid == c[1]).first():
                t = Course(c[0], c[1], account.platform_uuid)
                db.session.add(t)

        db.session.commit()

        for c in courses:
            sub = UserSubscriptions(user.id, c[1], account.platform_uuid)
            db.session.add(sub)

    db.session.add(account)
    db.session.commit()

    return make_response(0, "OK", {"id": account.id})


@bp.route("/list", methods=['POST', 'GET'])
def list_account():
    """
    返回当前用添加的所有账户
    :return: make_response()
    return_data = {
        "account_list" -> list[{
                "id": int
                "userid": int
                "platform_uuid": str
                "fields": dict
            }
        ]
    }
    """
    user, data = get_context_user(data_required=False)

    account_count = len(user.accounts.all())
    return make_response(0, "OK", {"account_list": user.accounts.all(), "account_count": account_count})


@bp.route("/delete", methods=['POST', 'GET'])
def delete_account():
    """
    删除账户
    :return: make_response()
    return_data = {
        "id" -> int
    }
    """
    user, data = get_context_user()
    check_data(DeleteAccountRules, data)

    account = Account.query.get(data['id'])
    if account is None:
        return make_response(-1, "Id not found(nmsl)", {}, 404)
    if account.userid != user.id:
        return make_response(-1, "Cannot delete others' account(nmsl).", {}, 403)

    db.session.delete(account)

    subs = account.user.subscriptions.filter(UserSubscriptions.platform_uuid == account.platform_uuid).all()

    for sub in subs:
        db.session.delete(sub)

    db.session.commit()

    return make_response(0, "OK", {"id": account.id})



