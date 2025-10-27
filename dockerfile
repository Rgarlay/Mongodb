FROM python:3.10-slim-bookworm 

WORKDIR /app

COPY . /app

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install --default-timeout=200 -r req.txt 

RUN pip install python-multipart

CMD ["python3","app.py"]
