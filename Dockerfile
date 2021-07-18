From python:alpine
Run mkdir /loadBalancer
WORKDIR /loadBalancer
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

