from utils import get_context, standard_response
from main import app


@app.route("/todo/add")
def add_todo():
    """
    允许用户手动添加todo
    data:   "title" -> str (len 1 - 50)
            "content" -> str (len 1 - 200)
            "ddl_time" -> int
            "tag" -> str
            "course" -> str
    :return: standard_response()
    """
    open_id, data = get_context()
    if not data['title']:
        return standard_response(-1, "请输入增加todo的名称", {})

    if not data['ddl_time']:
        return standard_response(-1, "请输入ddl截止时间", {})
    return standard_response(0, "OK", {})


@app.route("/todo/list")
def list_todo():
    open_id, data = get_context()

    return standard_response(0, "OK", {})


@app.route("/todo/delete")
def delete_todo():
    open_id, data = get_context()

    return standard_response(0, "OK", {})

