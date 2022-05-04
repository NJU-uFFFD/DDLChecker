from flask import Flask

# 所有的 @app.route 分类写到 routes 文件夹下的模块中
from routes import *

from config import *

from db import db

WX_APPID = ""


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(ddl.bp)
app.register_blueprint(account.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_ADDRESS}/{MYSQL_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.route("/")
def hello():
    return "hello!"


if __name__ == '__main__':
    app.run()
