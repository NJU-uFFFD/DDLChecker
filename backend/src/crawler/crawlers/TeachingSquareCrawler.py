import hashlib
import json
import logging
import time
import uuid

import html2text
import requests

from ..Crawler import Crawler
from ..CrawlerException import LoginException, UnknownCrawlerException

TEACHING_SQUARE_CRAWLER_UUID = "f15684f5-d870-4a9d-b859-e7eec3c6e3b5"


class TeachingSquareCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.session = None
        self.login_data = None
        self.token = None
        self.uid = None

    @staticmethod
    def required_fields():
        return {"account": {"name": "账号", "detail": "教学立方账号"},
                "password": {"name": "密码", "detail": "教学立方密码"}}

    def renew_session_if_expired(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.88 Safari/537.36'
        })
        hl = hashlib.md5()
        hl.update(self.login_data['password'].encode("utf-8"))
        r = self.session.post("https://teaching.applysquare.com/Api/User/ajaxLogin", data={
            "email": self.login_data['account'],
            "password": hl.hexdigest()
        }).json()

        logging.info(r)

        if r['status'] != 70000:
            raise LoginException(str(r['message']))

        self.token = r['message']['token']
        self.uid = r['message']['uid']

    def login(self, login_data: dict):
        self.login_data = login_data
        self.renew_session_if_expired()

    def fetch_course(self) -> list:
        # 获取课程列表
        r = requests.get(
            f"https://teaching.applysquare.com/Api/Public/getIndexCourseList/token/{self.token}?type=1&usertype=1&uid={self.uid}").json()
        logging.info(r)

        print(json.dumps(r))

        if r['status'] != 70000:
            raise UnknownCrawlerException("非成功返回值: " + json.dumps(r))

        return [(course['name'] + " " + course['class_name'], str(uuid.uuid5(uuid.UUID(TEACHING_SQUARE_CRAWLER_UUID), course['cid']))) for course in r['message']]

    def fetch_ddl(self) -> list:
        # 获取课程列表
        r = requests.get(
            f"https://teaching.applysquare.com/Api/Public/getIndexCourseList/token/{self.token}?type=1&usertype=1&uid={self.uid}").json()
        logging.info(r)

        if r['status'] != 70000:
            raise UnknownCrawlerException("非成功返回值: " + json.dumps(r))

        temp = []

        for course in r['message']:
            r = requests.get(
                f"https://teaching.applysquare.com/Api/Work/getWorkList/token/{self.token}?plan_id=-1&page=1&uid={self.uid}&cid={course['cid']}").json()
            logging.info(r)
            if r['status'] != 1:
                raise UnknownCrawlerException("非成功返回值: " + json.dumps(r))
            for work in r['message']['list']:
                # if work['step'] == '未完成':
                r = requests.get(
                    f"https://teaching.applysquare.com/Api/Work/getHomeworkInfo/token/{self.token}?homework_id={work['content']}&uid={self.uid}&cid={course['cid']}").json()

                content = "未获取到内容, 请到教学立方上查看."
                try:
                    content = html2text.html2text(r['message']['question_list'][0]['content'])
                except:
                    logging.info("获取具体内容出错: " + json.dumps(r))

                temp.append({"platform_uuid": TEACHING_SQUARE_CRAWLER_UUID,
                             "course_uuid": str(uuid.uuid5(uuid.UUID(TEACHING_SQUARE_CRAWLER_UUID), course['cid'])),
                             "create_time": int(work['publish_at']) * 1000,
                             "ddl_time": int(
                                 time.mktime(time.strptime(work['submit_at'], '%Y-%m-%d %H:%M')) * 1000),
                             "title": work['homework_title'],
                             "content": content})

        return temp
