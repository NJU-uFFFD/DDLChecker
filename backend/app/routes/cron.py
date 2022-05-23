from flask import Blueprint, request

import service.cron
from config import INVOKE_PATH_TOKEN

bp = Blueprint("cron", __name__, url_prefix="/invoke")


@bp.route('/')
def invoke():
    assert request.get_json()['cron_token'] == INVOKE_PATH_TOKEN, "Invalid cron token."
    service.cron.cron_work()
