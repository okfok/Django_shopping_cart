# syntax=docker/dockerfile:1

FROM python:3.10
WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ShoppingCart .


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]