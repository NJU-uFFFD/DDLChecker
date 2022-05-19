from flask import Flask
from routes import *
from config import *
from db import db


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(ddl.bp)
app.register_blueprint(account.bp)
app.register_blueprint(user.bp)
app.register_blueprint(community.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_ADDRESS}/{MYSQL_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return "hello!"


if __name__ == '__main__':
    app.run()
