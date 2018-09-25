FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /app/backend
ADD backend/requirements.txt .
RUN pip install -r requirements.txt
ADD . /app/
