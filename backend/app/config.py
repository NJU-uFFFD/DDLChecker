import os

# 默认配置
MYSQL_ADDRESS = os.environ.get('MYSQL_ADDRESS') or 'sh-cynosdbmysql-grp-e2da81to.sql.tencentcdb.com:27821'
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME') or 'root'
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'g6jVKKbc'
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'DDLChecker'

APP_ID = ""
APP_SECRET = ""
