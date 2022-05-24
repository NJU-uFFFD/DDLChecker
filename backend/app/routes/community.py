from flask import Blueprint
from routes.utils import get_context, check_data, make_response
from db.course import Course
from db.source_ddl import SourceDdl


bp = Blueprint("community", __name__, url_prefix="/community")






