From python:alpine
Run mkdir /loadBalancer
WORKDIR /loadBalancer
COPY code/requirements.txt .
RUN pip install -r requirements.txt
COPY code .

