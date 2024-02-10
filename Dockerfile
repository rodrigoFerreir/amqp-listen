FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update -y \
    && apt-get upgrade -y \
    && chmod 777 -R .\
    && pip install -r requirements.txt 

COPY . .

CMD [ "python", "api.py" ]