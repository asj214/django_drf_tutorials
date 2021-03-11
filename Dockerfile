FROM python:3.9

ENV PYTHONUNBUFFERED 0

WORKDIR /workspace/django_drf_tutorials

COPY requirements.txt ./
# RUN apt-get update && apt-get install -y zlib1g-dev libicu-dev g++ locales gettext
RUN apt-get update && apt-get install -y gettext
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000