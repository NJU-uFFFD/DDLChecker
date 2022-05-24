import base64
import logging
import random
import re
import string

import requests
from Crypto.Cipher import AES
from config import OCR_API_URL
from crawler.Crawler import Crawler

from crawler.CrawlerException import LoginException


NJU_SPOC_UUID = "68dc1014-7bfe-4ea3-a000-5734303d9f59"


class NjuSpocCrawler(Crawler):
    def __encrypt_password(self, password):
        """
        逆向 javascript 得到的加密代码
        :param password: 密码
        :return: 加密后的密码
        """
        random_iv = ''.join(random.sample((string.ascii_letters + string.digits) * 10, 16))
        random_str = ''.join(random.sample((string.ascii_letters + string.digits) * 10, 64))

        data = random_str + password
        key = self.pwd_salt.encode("utf-8")
        iv = random_iv.encode("utf-8")

        bs = AES.block_size

        def pad(s):
            return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = cipher.encrypt(pad(data).encode("utf-8"))
        return base64.b64encode(data).decode("utf-8")

    def __need_captcha(self, username):
        url = 'https://authserver.nju.edu.cn/authserver/needCaptcha.html?username={}'.format(
            username)
        r = self.session.post(url)
        return 'true' in r.text

    def __new_session(self):
        """
        创建一个新的 session
        :return: None
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.88 Safari/537.36'
        })

        r = self.session.get("https://authserver.nju.edu.cn/authserver/login")
        self.lt = re.search(
            r'<input type="hidden" name="lt" value="(.*)"/>', r.text).group(1)
        self.execution = re.search(
            r'<input type="hidden" name="execution" value="(.*)"/>', r.text).group(1)
        self.event_id = re.search(
            r'<input type="hidden" name="_eventId" value="(.*)"/>', r.text).group(1)
        self.rm_shown = re.search(
            r'<input type="hidden" name="rmShown" value="(.*)"', r.text).group(1)
        self.pwd_salt = re.search(
            r'<input type="hidden" id="pwdDefaultEncryptSalt" value="(.*)"', r.text).group(1)

    def __get_captcha_code(self):
        url = 'https://authserver.nju.edu.cn/authserver/captcha.html'
        res = self.session.get(url)
        return base64.b64encode(res.content)

    def login(self, fields: dict) -> None:
        """
        登录南大统一身份认证
        登录成功不返回内容, 登录失败抛出异常
        """
        self.__new_session()

        username = fields['account']
        password = fields['password']

        captcha = ""
        if self.__need_captcha(username):
            captcha = requests.post(OCR_API_URL, data=self.__get_captcha_code()).json()['result']

        data = {
            'username': username,
            'password': self.__encrypt_password(password),
            'lt': self.lt,
            'dllt': 'userNamePasswordLogin',
            'execution': self.execution,
            '_eventId': self.event_id,
            'rmShown': self.rm_shown,
            'captchaResponse': captcha
        }
        r = self.session.post("https://authserver.nju.edu.cn/authserver/login", data=data,
                              allow_redirects=False)
        logging.info(r.text)

        if r.status_code == 200:
            raise LoginException("用户名或密码错误?")
        elif r.status_code == 302:
            # 登录成功
            try:
                r = self.session.get("https://study.nju.edu.cn/oauth/toMoocAuth.mooc")
                logging.info(self.session.cookies)
                r = self.session.post("https://study.nju.edu.cn/portal/user/hasmessage.mooc", data={
                    "postoken": self.session.cookies.get("cpstk")
                }, headers={
                    "Referer": "https://study.nju.edu.cn/portal/myCourseIndex/1.mooc?checkEmail=false"
                })
                logging.info(r.text)
            except Exception as e:
                logging.debug(str(e))
                raise LoginException("SPOC 平台登录失败, 请稍后再试.")
        else:
            raise LoginException("未知错误, 请稍后再试: " + str(r.status_code))

    @staticmethod
    def required_fields() -> dict:
        """
        登录需要的信息
        :return:
        """
        return {"account": {"name": "账号", "detail": "南大统一认证登录账号"},
                "password": {"name": "密码", "detail": "南大统一认证登录密码"}}

    def fetch_course(self) -> list:
        pass

    def fetch_ddl(self) -> list:
        """
        获取 ddl
        :return: ddl list
        """
        return []
