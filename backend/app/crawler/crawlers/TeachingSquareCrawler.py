import hashlib
import logging

import requests

from ..Crawler import Crawler
from ..CrawlerException import LoginException


class TeachingSquareCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.session = None
        self.login_data = None

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

    def login(self, login_data: dict):
        self.login_data = login_data
        self.renew_session_if_expired()

    def fetch_ddl(self) -> list:
        # todo
        return []
