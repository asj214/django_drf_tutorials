# django_drf_tutorials  
django, drf, tutorial

### 개발 환경  
- python: 3.9
- django: 3.1.4
- mysql: 5.8

### 주요 패키지  
- [Django](https://docs.djangoproject.com/ko/3.1/intro/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Extensions](https://django-extensions.readthedocs.io/en/latest/)


### 가상화 Mac  
```sh
# create venv
python -m venv .venv

# activate
. .venv/bin/activate

# deactivate
deactivate
```

### 가상화 Windows  
```sh
# create venv
python -m venv venv

# activate
venv\Scripts\activate

# deactivate
deactivate
```

### 설치  
```sh
# clone & move
git clone git@github.com:asj214/django_drf_tutorials.git && cd django_drf_tutorials

# virtualenv
. .venv/bin/activate

# pip upgrade
python -m pip install --upgrade pip

# package install
pip install -r requirements.txt
```

### .env 
```sh
cp .env.example .env
```

### database migration  
```sql
CREATE DATABASE `django_drf_tutorials`;
```
```sh
python manage.py migrate
```

### run  
```sh
python manage.py runserver
# or
python manage.py runserver_plus
# or
gunicorn --bind 0.0.0.0:8000 system.wsgi:application
```

### commands  
```sh
# create new app Ex. post
django-admin startapp post

# database make migration all app
python manage.py makemigrations

# database make migration post app
python manage.py makemigrations post

# migrate
python manage.py migrate
```

### seeds  
```sh
# user seed ex. create user 100
python manage.py user_seed --times 100

# post seed ex. create post 10000
python manage.py post_seed --times 10000

# comment seed ex. create comment 100000
python manage.py comment_seed --times 100000
```
