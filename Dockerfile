FROM python:3.8

RUN apt-get update && \
    apt install -y vim \
    git 

WORKDIR /home/src

COPY requirements.txt /home/src

RUN pip3 install -r requirements.txt

EXPOSE 5000
