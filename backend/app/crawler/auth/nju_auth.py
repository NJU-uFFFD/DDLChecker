import base64
import random
import re
import string
from Crypto.Cipher import AES

import requests

from crawler.auth import LoginException


class NjuAuth:
    def __init__(self):
        self.__new_session()

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

    def login(self, username: str, password: str) -> None:
        """
        登录南大统一身份认证
        登录成功不返回内容, 登录失败抛出异常
        :param username: 南大统一身份认证用户名
        :param password: 南大统一身份认证密码
        """
        self.__new_session()

        if self.__need_captcha(username):
            raise LoginException("南大统一身份认证登录需要验证码，可能是因为上次登录输入了错误的密码，"
                                 "请尝试打开 https://authserver.nju.edu.cn/ 手动登录一次后再试。")

        data = {
            'username': username,
            'password': self.__encrypt_password(password),
            'lt': self.lt,
            'dllt': 'userNamePasswordLogin',
            'execution': self.execution,
            '_eventId': self.event_id,
            'rmShown': self.rm_shown
        }
        r = self.session.post("https://authserver.nju.edu.cn/authserver/login", data=data,
                              allow_redirects=False)

        if r.status_code == 200:
            raise LoginException("用户名或密码错误？")
        elif r.status_code == 302:
            # 登录成功
            return
        else:
            raise LoginException("未知错误，请稍后再试：" + str(r.status_code))
