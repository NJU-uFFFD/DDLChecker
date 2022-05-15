import time


class Crawler:
    def __init__(self):
        pass

    def required_fields(self) -> dict:
        """
        登录需要的信息
        :return:
        """
        return {"account": {"name": "账号", "detail": "登录账号"},
                "password": {"name": "密码", "detail": "登录密码"}}

    def login(self, login_data: dict):
        """
        登录账号, 登录失败抛出异常
        :param login_data:
        :return:
        """

    def fetch_ddl(self) -> list:
        """
        获取 ddl
        :return: ddl list
        """
        return []
