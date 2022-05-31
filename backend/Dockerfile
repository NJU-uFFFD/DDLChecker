FROM python:3.9.13-slim-buster

WORKDIR /app
COPY ./src /app

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]
