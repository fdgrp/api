FROM python:3.9-slim

EXPOSE 8080

RUN pip install sbeaver mysql-connector-python requests

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN cp cfg.example.py cfg.py

CMD [ "python", "./main.py"]