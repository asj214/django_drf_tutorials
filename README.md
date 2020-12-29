# django_drf_tutorials  
django, drf, tutorial

### 개발 환경  
- python: 3.9
- django: 3.1.4
- mysql: 5.8

### 설치  
```sh
# clone & move
git clone git@github.com:asj214/django_drf_tutorials.git && cd django_drf_tutorials

# virtualenv
python -m venv .venv

# activate
. .venv/bin/activate

# pip upgrade
python -m pip install --upgrade pip

# package install
pip install -r requirements.txt
```

### settings.py 작성  
```python
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DJANGO_DB_NAME', 'django_drf_tutorials'),
        'USER': os.environ.get('DJANGO_DB_USERNAME', 'root'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DJANGO_DB_PORT', '3306'),
        'OPTIONS': {'charset': 'utf8mb4',},
    }
}
```

### database migration  
```sql
CREATE DATABASE django_drf_tutorials;
```
```sh
python manage.py migrate
```

### run  
```sh
python manage.py runserver
# or
python manage.py runserver_plus
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