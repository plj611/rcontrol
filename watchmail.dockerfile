FROM python:3.8-buster

ARG USERID
ARG GROUPID
# RUN mkdir /opt/code

WORKDIR /opt/code

COPY requirements.txt /opt/code/requirements.txt

RUN pip install -r /opt/code/requirements.txt && \
    addgroup --gid ${GROUPID} pl && \
    adduser --uid ${USERID} --gid ${GROUPID} pl 

USER pl

CMD [ "python", "watchmail.py" ]