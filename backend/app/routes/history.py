import time

from flask import Blueprint
from routes.utils import get_context_user, make_response
from db.ddl import Ddl

bp = Blueprint("history", __name__, url_prefix="/history")


@bp.route("/stat", methods=["GET", "POST"])
def stat():
    user, data = get_context_user(data_required=False)

    ddls = user.ddls.all()
    completed_count = user.ddls.filter(Ddl.is_completed == True).count()
    ddl_count = user.ddls.count()
    urgent_count = user.ddls.filter(Ddl.tag == "紧急").count()
    overtime_count = user.ddls.filter(Ddl.ddl_time < round(time.time() * 1000)).count()

    complete_rate = 1 if ddl_count == 0 else completed_count / ddl_count

    first_time = time.time()
    last_time = time.time()
    average_complete_time_percentage = 0
    if ddls is not None:
        total_time = 0
        total_complete_time = 0
        for i in ddls:
            if i.ddl_time - i.create_time > 0:
                total_time += (i.ddl_time - i.create_time)
                if i.is_completed:
                    total_complete_time += (i.complete_time - i.create_time)
        average_complete_time_percentage = total_complete_time / total_time if total_time != 0 else 0
        first_time = min(user.ddls.filter(Ddl.ddl_time != None).order_by(Ddl.ddl_time).first().ddl_time,
                         user.ddls.filter(Ddl.create_time != None).order_by(Ddl.create_time).first().create_time,
                         user.ddls.filter(Ddl.complete_time != None).order_by(Ddl.complete_time).first().complete_time)
        last_time = max(user.ddls.filter(Ddl.ddl_time != None).order_by(Ddl.ddl_time.desc()).first().ddl_time,
                        user.ddls.filter(Ddl.create_time != None).order_by(Ddl.create_time.desc()).first().create_time,
                        user.ddls.filter(Ddl.complete_time != None).order_by(Ddl.complete_time.desc()).first().complete_time)

    return make_response(0, "OK", {"completed_count": completed_count, "urgent_count": urgent_count,
                                   "overtime_count": overtime_count, "completed_rate": complete_rate,
                                   "average_complete_time_percentage": average_complete_time_percentage,
                                   "first_time": first_time, "last_time": last_time})
