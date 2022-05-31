FROM python:3.9.13-slim-buster

WORKDIR /app
COPY ./src /app

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

RUN Deps="libmariadb-dev" \
    && mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb http://mirrors.cloud.tencent.com/debian/ buster main non-free contrib" > /etc/apt/sources.list \
    && apt-get update \
    && apt-get install $Deps --no-install-recommends --no-install-suggests -y  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /etc/apt/sources.list \
    && mv /etc/apt/sources.list.bak /etc/apt/sources.list

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]
