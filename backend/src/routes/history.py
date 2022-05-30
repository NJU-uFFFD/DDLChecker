import logging
import time

from flask import Blueprint
from routes.utils import get_context_user, make_response
from db.ddl import Ddl

bp = Blueprint("history", __name__, url_prefix="/history")


@bp.route("/stat", methods=["GET", "POST"])
def stat():
    user, data = get_context_user(data_required=False)

    ddls = user.ddls.filter().all()
    completed_count = user.ddls.filter(Ddl.is_completed == True).count()
    ddl_count = user.ddls.filter().count()
    urgent_count = user.ddls.filter(Ddl.tag == "紧急", Ddl.is_completed == False).count()
    overtime_count = user.ddls.filter(Ddl.ddl_time < round(time.time() * 1000), Ddl.is_completed == False).count()

    complete_rate = 1 if ddl_count == 0 else completed_count / ddl_count

    calendar_mark_set = set()

    average_complete_time_percentage = 0

    first_time = int(time.time() * 1000)
    last_time = int(time.time() * 1000)
    if ddl_count > 0:
        total_time = 0
        total_complete_time = 0
        for i in ddls:

            calendar_mark_set.add(time.strftime("%Y/%m/%d", time.localtime(i.create_time // 1000)))
            if i.ddl_time is not None: calendar_mark_set.add(time.strftime("%Y/%m/%d", time.localtime(i.ddl_time // 1000)))
            if i.complete_time is not None: calendar_mark_set.add(time.strftime("%Y/%m/%d", time.localtime(i.complete_time // 1000)))

            if i.ddl_time - i.create_time > 0:
                total_time += (i.ddl_time - i.create_time)
                if i.is_completed:
                    total_complete_time += (i.complete_time - i.create_time)
        average_complete_time_percentage = total_complete_time / total_time if total_time != 0 else 0

        safe = lambda value, attr, default: default if value is None else value.__getattribute__(attr)

        # if user.ddls.filter(Ddl.ddl_time != None).order_by(Ddl.ddl_time).first() is not None:
        #     first_time_compare_list.append()
        try:
            first_time = min(safe(user.ddls.filter(Ddl.ddl_time != None).order_by(Ddl.ddl_time).first(), 'ddl_time', 1919810810810810810810),
                             safe(user.ddls.filter(Ddl.create_time != None).order_by(Ddl.create_time).first(), 'create_time', 1919810810810810810810),
                             safe(user.ddls.filter(Ddl.complete_time != None).order_by(Ddl.complete_time).first(), 'complete_time', 1919810810810810810810))
            last_time = max(safe(user.ddls.filter(Ddl.ddl_time != None).order_by(Ddl.ddl_time.desc()).first(), 'ddl_time', -114514),
                            safe(user.ddls.filter(Ddl.create_time != None).order_by(Ddl.create_time.desc()).first(), 'create_time', -114514),
                            safe(user.ddls.filter(Ddl.complete_time != None).order_by(Ddl.complete_time.desc()).first(), 'complete_time', -114514))
            assert first_time != 1919810810810810810810, "nmsl"
            assert last_time != -114514, "nmsl"
        except (TypeError, AttributeError) as e:
            logging.error(e)
            first_time = int(time.time() * 1000)
            last_time = int(time.time() * 1000)


        calendar_mark_list = []
        for s in calendar_mark_set:
            calendar_mark_list.append({"value": s})

    return make_response(0, "OK", {"completed_count": completed_count, "urgent_count": urgent_count,
                                   "overtime_count": overtime_count, "completed_rate": complete_rate,
                                   "average_complete_time_percentage": average_complete_time_percentage,
                                   "first_time": first_time, "last_time": last_time, "calendar_mark": calendar_mark_list})
