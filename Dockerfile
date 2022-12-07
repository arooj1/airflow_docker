FROM python:latest
#LABEL Name=wp-runner

ENV HTTP_PROXY "http://fastweb.int.bell.ca:8083/"
ENV HTTPS_PROXY "http://fastweb.int.bell.ca:8083/"
ENV http_proxy "http://fastweb.int.bell.ca:8083/"
ENV https_proxy "http://fastweb.int.bell.ca:8083/"

#WORKDIR /whitespace/

RUN apt-get -y update
# RUN apt-get -y install build-essential
# RUN apt -y install libpq-dev
RUN apt-get install -y vim wget git 

COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .
