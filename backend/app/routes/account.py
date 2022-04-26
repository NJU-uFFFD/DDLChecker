from crypt import methods
from utils import get_context, standard_response
from main import app
from flask import request
import json


@app.route("/account/add", methods=["POST"])
def add_account():
    data, open_id = get_context()

    return standard_response(0, "OK", {})


@app.route("/account/list", methods=["POST"])
def list_account():
    data, open_id = get_context()

    return


@app.route("/account/delete", methods=["POST"])
def delete_account():
    data, open_id = get_context()

    return
