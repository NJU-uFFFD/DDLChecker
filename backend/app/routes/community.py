from flask import Blueprint
from routes.utils import get_context, check_data, make_response
from db.userSubs import UserSubscriptions
from db.sourceDdl import SourceDdl
from db.course import Course
from db.account import Account


bp = Blueprint("community", __name__, url_prefix="/community")






