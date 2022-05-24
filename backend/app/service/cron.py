import json
import logging
import random

from db import db
from db.account import Account
from db.course import Course
from crawler.util import list_crawlers
from db.sourceDdl import SourceDdl

from util.encrypt import aes_decrypt


already_done = set()


# 定时任务, 需要每过一定时间被触发
def cron_work():
    for c in Course.query.all():

        if c.platform_uuid in already_done:
            continue

        # 查找爬虫对象
        crawler_obj = None

        for i in list_crawlers():
            if i['uuid'] == c.platform_uuid:
                crawler_obj = i['obj']

        crawler = crawler_obj()

        # 找一个幸运用户的账号爬数据
        lucky_account = random.choice(c.subscriptions.all()).user.accounts.filter(Account.platform_uuid == c.platform_uuid).first()

        fields = json.loads(aes_decrypt(lucky_account.fields))
        crawler.login(fields)

        ddls = crawler.fetch_ddl()
        logging.info(ddls)

        # 保存 ddl
        for ddl in ddls:
            already_done.add(ddl.course_uuid)

            newest = SourceDdl.query.order_by(SourceDdl.create_time.desc()).first()
            if ddl.create_time > newest:
                t = SourceDdl(c.course_uuid, c.platform_uuid, ddl.title, ddl.content, "[]", ddl.ddl_time, ddl.create_time)
                db.session.add(t)

        db.session.commit()


    return "success"
