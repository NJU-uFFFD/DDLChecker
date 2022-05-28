import time

from flask import Blueprint
from routes.utils import get_context_user, make_response
from db.ddl import Ddl

bp = Blueprint("history", __name__, url_prefix="/history")


@bp.route("/stat", methods=["GET", "POST"])
def stat():
    user, data = get_context_user(data_required=False)

    completed_count = user.ddls.filter(Ddl.is_completed == True).count()
    ddl_count = user.ddls.count()
    urgent_count = user.ddls.filter(Ddl.tag == "紧急").count()
    overtime_count = user.ddls.filter(Ddl.ddl_time < round(time.time() * 1000)).count()

    complete_rate = 1 if ddl_count == 0 else completed_count / ddl_count

    return make_response(0, "OK", {"completed_count": completed_count, "urgent_count": urgent_count, "overtime_count": overtime_count, "completed_rate": complete_rate})
