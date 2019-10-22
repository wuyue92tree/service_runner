FROM wuyue/python3-app:with_nginx
LABEL maintainer="wuyue92tree@163.com"

COPY . /data/src
COPY ./deploy.ini /etc/supervisor/conf.d/
COPY ./_product/nginx.conf /usr/local/nginx/conf/nginx.conf

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

RUN python manage.py initdb

WORKDIR /data/src

EXPOSE 9001
EXPOSE 80
