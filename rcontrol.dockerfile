FROM python:3.8-buster

# RUN mkdir /opt/code

WORKDIR /opt/code

COPY requirements.txt /opt/code/requirements.txt

RUN pip install -r /opt/code/requirements.txt

EXPOSE 5000

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0"]