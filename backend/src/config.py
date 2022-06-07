import os

# 默认配置
MYSQL_ADDRESS = os.environ.get('MYSQL_ADDRESS')
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')

INVOKE_PATH_TOKEN = os.environ.get('CRON_TOKEN')

OCR_API_URL = "https://dddd-ocr-ddddocr-dgszqoojqy.cn-shanghai.fcapp.run/ocr/b64/json"

ENCRYPT_KEY = "eUDin9Qu135wsC2szsZcRSgGqYKDomQs".encode("utf-8")
ENCRYPT_IV = "1145141919810520".encode("utf-8")

APP_ID = ""
APP_SECRET = ""
