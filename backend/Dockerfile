FROM python:3.9.13-slim-buster

WORKDIR /app
COPY ./src /app

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

RUN Deps="libmariadb-dev python3-dev gcc" \
    && sed -i s@/deb.debian.org/@/mirrors.cloud.tencent.com/@g /etc/apt/sources.list \
    && apt-get update \
    && apt-get install $Deps --no-install-recommends --no-install-suggests -y  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

CMD ["gunicorn", "app:app"]
