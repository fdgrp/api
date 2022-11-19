FROM python:3.9-slim

EXPOSE 8080

COPY . /usr/src/app

WORKDIR /usr/src/app


RUN pip install sbeaver mysql-connector-python requests

RUN "echo '' > cfg.py" 

CMD [ "python", "./server.py"]