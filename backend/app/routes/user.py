import random

from flask import Blueprint
from db.user import User
from routes.utils import get_context, make_response, check_data
from routes.rules.user_rules import *
from db import db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    """
    登录接口, 每次用户打开小程序时调用
    """
    openid, data = get_context()
    check_data(RegisterRules, data)

    new_user = False

    user = User.query.filter(User.openid == openid).first()
    if user is None:
        new_user = True
        user = User(openid, data.get('username') or "用户" + str(random.randint(100000000, 999999999)))
        db.session.add(user)
        db.session.commit()

    return make_response(0, "OK", {"userid": user.id, "username": user.username, "new": new_user})
