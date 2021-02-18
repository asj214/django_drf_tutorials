FROM python:3.9

ENV PYTHONUNBUFFERED 0

WORKDIR /workspace/django_drf_tutorials

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000