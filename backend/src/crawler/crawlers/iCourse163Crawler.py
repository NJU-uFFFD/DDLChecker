import logging
import time
import uuid

import requests

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
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions
        from selenium.webdriver.support.wait import WebDriverWait

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

            # time.sleep(5)

            login_frame = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//div[@class="ux-login-set-container"]/iframe'))
            )

            driver.switch_to.frame(login_frame)

            username_input = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入手机号"]'))
            )

            password_input = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入密码"]'))
            )

            username_input.send_keys(self.login_data['account'])
            password_input.send_keys(self.login_data['password'])

            submit_btn = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.ID, "submitBtn"))
            )

            time.sleep(1)
            submit_btn.click()

            for _ in range(0, 12):
                time.sleep(1)
                if driver.current_url == "https://www.icourse163.org/":
                    break
            else:
                logging.info(driver.current_url)
                assert False, "登录失败! 可能是网络问题或需要验证码."

            cookies = driver.get_cookies()
            temp = {}

            for ck in cookies:
                temp[ck['name']] = ck['value']

            self.session.cookies = requests.utils.cookiejar_from_dict(temp)

        r = self.session.post("https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc",
                              params={
                                  "csrfKey": self.session.cookies.get("NTESSTUDYSI")
                              }, data={
                "type": 30,
                "p": 1,
                "psize": 1,
                "courseType": 1
            })

        assert r.json()['code'] == 0, "Cookie 无效."

    def login(self, login_data: dict):
        self.login_data = login_data
        self.renew_session_if_expired()

    def __fetch_course(self) -> list:
        # 暂定只爬取 SPOC, 因为 MOOC 好像不计分
        r = self.session.post("https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc",
                              params={
                                  "csrfKey": self.session.cookies.get("NTESSTUDYSI")
                              }, data={
                "type": 30,
                "p": 1,
                "psize": 60,
                "courseType": 2
            })

        return r.json()['result']['result']

    def fetch_course(self) -> list:
        t = self.__fetch_course()
        # print(t)
        temp = []
        for i in t:
            temp.append((i['name'], str(uuid.uuid5(uuid.UUID(ICOURSE163_UUID), str(i['termPanel']['fromTermId'])))))
        return temp

    def fetch_ddl(self) -> list:
        courses = self.__fetch_course()
        print(courses)
        temp = []
        for c in courses:
            r = self.session.post("https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc", params={
                "csrfKey": self.session.cookies.get("NTESSTUDYSI")
            }, data={
                "termId": c['termPanel']['fromTermId']
            })

            r = r.json()['result']['mocTermDto']

            for i in r['chapters']:
                for j in (i['homeworks'] or []) + (i['quizs'] or []):
                    try:
                        temp.append({
                            "platform_uuid": ICOURSE163_UUID,
                            "course_uuid": str(uuid.uuid5(uuid.UUID(ICOURSE163_UUID), str(c['termPanel']['fromTermId']))),
                            "create_time": j['test']['releaseTime'],
                            "ddl_time": j['test']['deadline'],
                            "title": i['name'] + j['name'],
                            "content": "来自中国大学 MOOC 的 `" + c['name'] + "` 课程 " + i['name']
                        })
                    except Exception as e:
                        logging.error(e)

            for i in r['exams']:
                try:
                    temp.append({
                        "platform_uuid": ICOURSE163_UUID,
                        "course_uuid": str(uuid.uuid5(uuid.UUID(ICOURSE163_UUID), str(c['termPanel']['fromTermId']))),
                        "create_time": i['releaseTime'],
                        "ddl_time": i['deadline'],
                        "title": c['name'] + i['name'],
                        "content": "来自中国大学 MOOC 的 `" + c['name'] + "` 课程: " + i['description']
                    })
                except Exception as e:
                    logging.error(e)

        now = int(time.time() * 1000)
        temp = [i for i in temp if i['ddl_time'] > now]

        return temp
