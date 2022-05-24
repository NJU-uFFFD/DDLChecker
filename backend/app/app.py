from flask import Flask
from routes import *
from config import *
from db import db
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask import request
import service

WX_APPID = ""

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(ddl.bp)
app.register_blueprint(account.bp)
app.register_blueprint(user.bp)
app.register_blueprint(community.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_ADDRESS}/{MYSQL_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
# with app.app_context():
#     db.drop_all()
#     db.create_all()


# 访问频率限制
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute", "3 per second"]
)


@app.route("/")
def hello():
    return "hello!"


@app.route('/invoke')
def invoke():
    assert request.get_json()['cron_token'] == INVOKE_PATH_TOKEN, "Invalid cron token."
    service.cron.cron_work()


if __name__ == '__main__':
    app.run()
    # import crawler.crawlers.TeachingSquareCrawler
    # c = crawler.crawlers.TeachingSquareCrawler.TeachingSquareCrawler()
    # c.login({"account": "18015503001", "password": "98324364xue"})
    # print(c.fetch_ddl())


