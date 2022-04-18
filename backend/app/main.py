from flask import Flask

# 所有的 @app.route 分类写到 routes 文件夹下的模块中
from routes import *

WX_APPID = ""


app = Flask(__name__)

if __name__ == '__main__':
    app.run()
