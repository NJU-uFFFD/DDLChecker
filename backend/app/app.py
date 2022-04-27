from flask import Flask

# 所有的 @app.route 分类写到 routes 文件夹下的模块中
from routes import *

WX_APPID = ""


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(ddl.bp)
app.register_blueprint(account.bp)


@app.route("/")
def hello():
    return "hello!"


if __name__ == '__main__':
    app.run()
