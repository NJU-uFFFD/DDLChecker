from flask import Blueprint
from db.user import User
from routes.utils import get_context, make_response, check_data
from routes.rules.user_rules import *
from db import db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/register")
def register():
    open_id, data = get_context()
    check_data(RegisterRules, data)

    user = User.query.filter(User.openid == open_id, User.username == data['username']).first()
    if user is None:
        user = User(open_id, data['username'])
        db.session.add(user)
        db.session.commit()

    return make_response(0, "OK", {"userid": user.id})
