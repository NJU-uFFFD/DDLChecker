from crypt import methods

from flask import Blueprint
from routes.utils import get_context_user
from db.ddl import Ddl

bp = Blueprint("history", __name__, url_prefix="/history")


@bp.route("/stat", methods=["GET", "POST"])
def stat():
    user, data = get_context_user(data_required=False)

    user.ddl.filter(Ddl.is_completed == True)