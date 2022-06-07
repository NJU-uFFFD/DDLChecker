import json
import logging
import random
import time

from db import db
from db.account import Account
from db.course import Course
from crawler.util import list_crawlers
from db.ddl import Ddl
from db.sourceDdl import SourceDdl
from db.user import User
from db.userSubs import UserSubscriptions

from util.encrypt import aes_decrypt


def cron_work_daily():
    users = User.query.all()
    for u in users:
        u.account_add_times = 0

    db.session.commit()

    accounts = Account.query.all()
    for account in accounts:
        try:
            # 查找爬虫对象
            crawler_obj = None

            for i in list_crawlers():
                if i['uuid'] == account.platform_uuid:
                    crawler_obj = i['obj']

            crawler = crawler_obj()
            crawler.login(json.loads(aes_decrypt(account.fields)))
            courses = crawler.fetch_course()

            for c in courses:
                if not Course.query.filter(Course.course_uuid == c[1]).first():
                    t = Course(c[0], c[1], account.platform_uuid)
                    db.session.add(t)
            db.session.commit()

            for c in courses:
                if not UserSubscriptions.query.filter(UserSubscriptions.userid == account.userid,
                                                      UserSubscriptions.course_uuid == c[1]).first():
                    sub = UserSubscriptions(account.userid, c[1], account.platform_uuid)
                    db.session.add(sub)

            account.status = "账号状态正常"
            db.session.commit()

        except Exception as e:
            logging.exception(e)
            # db.session.rollback()
            account.status = "登录失败: " + str(e)
            db.session.commit()

    return "success"


# 定时任务, 需要每过一定时间被触发
def cron_work():
    already_done = set()

    now_time = int(time.time() * 1000)

    for c in Course.query.filter(Course.creator_id == None).all():
        for _ in range(0, 3):
            try:
                print(c)
                if c.course_uuid in already_done:
                    logging.info("already done, pass.")
                    break

                # 查找爬虫对象
                crawler_obj = None

                for i in list_crawlers():
                    if i['uuid'] == c.platform_uuid:
                        crawler_obj = i['obj']

                crawler = crawler_obj()

                # 找一个幸运用户的账号爬数据
                lucky_account = random.choice(c.subscriptions.all()).user.accounts.filter(
                    Account.platform_uuid == c.platform_uuid).first()

                fields = json.loads(aes_decrypt(lucky_account.fields))
                crawler.login(fields)

                courses = crawler.fetch_course()

                ddls = crawler.fetch_ddl()
                logging.info(ddls)

                all_courses_got = set()
                for ddl in ddls:
                    all_courses_got.add(ddl['course_uuid'])

                # 保存 ddl
                for course_uuid in all_courses_got:
                    if not Course.query.filter(Course.course_uuid == course_uuid).first():
                        logging.warning("course uuid not found, pass: " + course_uuid)
                        continue

                    newest_ddl = SourceDdl.query.filter(SourceDdl.course_uuid == course_uuid,
                                                        SourceDdl.creator_id == None).order_by(
                        SourceDdl.create_time.desc()).first()

                    newest = -1
                    if newest_ddl:
                        newest = newest_ddl.create_time

                    for ddl in ddls:
                        if ddl['create_time'] > newest and ddl['course_uuid'] == course_uuid:
                            if ddl['course_uuid'] in already_done:
                                continue

                            if SourceDdl.query.filter(SourceDdl.ddl_time == ddl['ddl_time'],
                                                      SourceDdl.course_uuid == ddl['course_uuid'],
                                                      SourceDdl.title == ddl['title'],
                                                      SourceDdl.content == ddl['content']).count() > 0:
                                continue

                            t = SourceDdl(ddl['course_uuid'], c.platform_uuid, ddl['title'], ddl['content'], "",
                                          ddl['ddl_time'], ddl['create_time'])
                            db.session.add(t)
                already_done = already_done.union(set([c[1] for c in courses]))

                db.session.commit()
            except Exception as e:
                logging.exception(e)
                # db.session.rollback()

    logging.info(">>> crawler done!")

    # 分发 DDL
    subs = UserSubscriptions.query.all()
    for sub in subs:
        # logging.info(sub)
        updated = sub.last_updated
        for ddl in SourceDdl.query.filter(SourceDdl.course_uuid == sub.course_uuid, SourceDdl.creator_id == None).all():
            if ddl.ddl_time > int(time.time() * 1000) and ddl.create_time > updated:
                to_add = Ddl(sub.userid, ddl.title, ddl.ddl_time, ddl.create_time, ddl.content, "",
                             sub.course_uuid, sub.platform_uuid, ddl.id)
                # logging.info("adding ddl: " + str(ddl))
                db.session.add(to_add)
        sub.last_updated = now_time
    db.session.commit()

    logging.info(">>> distribution done!")

    return "success"
