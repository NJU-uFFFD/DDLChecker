import hashlib

import requests

from crawler.auth import LoginException


class SquareAuth:
    def __init__(self):
        self.__new_session()

    def __new_session(self):
        self.login_data = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.88 Safari/537.36'
        })

    def login(self, username: str, password: str) -> None:
        """
        登录教学立方
        登录成功不返回内容, 登录失败抛出异常
        :param username: 教学立方用户名
        :param password: 教学立方密码
        """
        self.__new_session()

        hl = hashlib.md5()
        hl.update(password.encode("utf-8"))
        r = self.session.post("https://teaching.applysquare.com/Api/User/ajaxLogin", data={
            "email": username,
            "password": hl.hexdigest()
        }).json()

        if r['status'] == 70000:
            self.login_data = r['message']
            return
        else:
            raise LoginException(str(r['message']))
