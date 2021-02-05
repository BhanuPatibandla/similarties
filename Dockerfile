FROM python:3.6.7

MAINTAINER bhanu

ADD ./requirements.txt /tmp/

RUN pip install -U pip && pip install -r /tmp/requirements.txt

ADD ./ /similarities

ENV FLASK_APP /similarities/similarity_app.py

ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 5000

CMD flask run