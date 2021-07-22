From python:alpine
RUN cd /home

RUN apk add build-base

RUN mkdir -p /home/loadBalancer/in
RUN mkdir /home/loadBalancer/out
WORKDIR /home/loadBalancer
RUN pwd
COPY ./code/requirements.txt .
COPY ./code/pythonRequirements.txt .
RUN pip install -r requirements.txt
RUN pip install -r pythonRequirements.txt
COPY ./code/ .