FROM python:3.8-slim
WORKDIR /opt
COPY src/server.py .
RUN pip install --no-cache-dir mail-parser requests
CMD ["/usr/local/bin/python", "-u", "/opt/server.py"]
EXPOSE 1025/tcp
