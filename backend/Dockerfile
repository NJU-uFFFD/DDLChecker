FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /app
COPY ./app /app
COPY ./uwsgi.ini /app/uwsgi.ini
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

