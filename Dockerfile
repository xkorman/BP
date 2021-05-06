FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN python3 -m venv venv
COPY requirements.txt /code/
RUN python3 -m pip install -r requirements.txt
COPY . /code/
