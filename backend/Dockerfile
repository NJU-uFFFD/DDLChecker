FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
