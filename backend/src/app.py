import json

from flask import Flask


from routes import *
from config import *
from db import db
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from service.cron import cron_work, cron_work_daily

from flask import request
import service

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(ddl.bp)
app.register_blueprint(account.bp)
app.register_blueprint(user.bp)
app.register_blueprint(community.bp)
app.register_blueprint(history.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_ADDRESS}/{MYSQL_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    # db.drop_all()
    db.create_all()

# 访问频率限制
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute", "3 per second"]
)


@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == '127.0.0.1'


@app.route("/")
def hello():
    return "hello!"


@app.route('/invoke')
def invoke():
    # assert request.get_json()['cron_token'] == INVOKE_PATH_TOKEN, "Invalid cron token."

    # if "daily" in request.get_json():
    #     return cron_work_daily()
    cron_work_daily()
    return cron_work()


if __name__ == '__main__':
    app.run()
    # import crawler.crawlers.TeachingSquareCrawler
    # c = crawler.crawlers.TeachingSquareCrawler.TeachingSquareCrawler()
    # c.login({"account": "18015503001", "password": "98324364xue"})
    # print(c.fetch_course())
    # import crawler.crawlers.NjuSpocCrawler
    # c = crawler.crawlers.NjuSpocCrawler.NjuSpocCrawler()
    # c.login({"account": "211250076", "password": "Lyc_20030125"})
    # print(c.fetch_ddl())
    # import crawler.crawlers.iCourse163Crawler
    # c = crawler.crawlers.iCourse163Crawler.iCourse163Crawler()
    # c.login({"account": "13952420797", "password": "x3LY5NuixIcj"})
    # print(c.fetch_course())
    # print(c.fetch_ddl())

