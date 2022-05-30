import time

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from crawler.Crawler import Crawler


ICOURSE163_UUID = "69921ef9-fe15-4731-930d-b60a644da254"


class iCourse163Crawler(Crawler):
    def __init__(self):
        super().__init__()

    @staticmethod
    def required_fields() -> dict:
        return {"account": {"name": "账号", "detail": "中国大学MOOC注册手机号"},
                "password": {"name": "密码", "detail": "中国大学MOOC密码"}}

    def renew_session_if_expired(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.88 Safari/537.36'
        })

        from selenium import webdriver
        with webdriver.Chrome() as driver:

            driver.get("https://www.icourse163.org/member/login.htm#/webLoginIndex")

            back_btn = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "ux-login-set-scan-code_ft_back"))
            )
            back_btn.click()

            phone_login = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@class="ux-tabs-underline_hd"]/li[2]'))
            )
            phone_login.click()

            username_input = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "j-inputtext dlemail j-nameforslide"))
            )

            password_input = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "j-inputtext dlpwd"))
            )

            username_input.sendkeys(self.login_data['account'])
            password_input.sendkeys(self.login_data['password'])
            time.sleep(5)









    def login(self, login_data: dict):
        self.login_data = login_data
        self.renew_session_if_expired()

    def fetch_course(self) -> list:
        return []

    def fetch_ddl(self) -> list:
        return []
