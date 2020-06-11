FROM python:3.8-slim
MAINTAINER hex@umonkey.net
RUN pip install --no-cache-dir mail-parser requests
RUN mkdir -p /var/www/modules/Mailwarm /var/www/cache/mailwarm
WORKDIR /var/www
COPY src/server.py modules/Mailwarm/server.py
COPY service.conf /etc/supervisor/conf.d/server.conf
COPY runner.sh /opt/runner.sh
CMD ["/opt/runner.sh"]
EXPOSE 1025/tcp
