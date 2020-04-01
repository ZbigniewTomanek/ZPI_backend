FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/