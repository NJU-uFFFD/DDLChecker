import logging

from crawler.auth import LoginException
from crawler.auth.nju_auth import NjuAuth


class StudyNjuAuth:
    def __init__(self):
        self.session = None

    def login(self, nju_auth: NjuAuth) -> None:
        """
        登录南大 spoc 平台
        :param nju_auth: 已经登录成功的 NjuAuth 对象
        """
        r = nju_auth.session.get("https://study.nju.edu.cn/oauth/toMoocAuth.mooc")

        try:
            nju_auth.session.post("https://study.nju.edu.cn/portal/user/hasmessage.mooc").json()['messageCount']
            self.session = nju_auth.session
        except Exception as e:
            logging.debug(str(e))
            raise LoginException("SPOC 平台登录失败，请稍后再试。")
