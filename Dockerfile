FROM python:3.11-slim-buster
WORKDIR /code
ADD ./docker-scripts.sh /code/docker-scripts.sh
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
COPY requirements_docker.txt .
COPY requirements.txt .
COPY requirements_dev.txt .
COPY .env /code/.env
RUN pip3 install --upgrade pip && pip3 install -r requirements_docker.txt
ADD . /code
RUN python manage.py migrate
