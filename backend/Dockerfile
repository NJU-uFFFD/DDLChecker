FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /app
COPY ./app /app
COPY ./uwsgi.ini /app/uwsgi.ini
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

