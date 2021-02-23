# django drf tutorial

### 개발 환경
- python 3.9
- mysql 5.7
- redis
- docker

### install
```sh
git clone https://github.com/asj214/django_drf_tutorials.git

cd django_drf_tutorials

docker-compose up
```

### .vscode/launch.json (for vscode debug)
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 3000
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/workspace/django_tutorials"
                }
            ]
        }
    ]
}
```

### 자주 사용하는 docker commands
```sh
# docker 멈추기, 컨테이너 삭제, 이미지 삭제
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)

# docker 상태
docker ps

# docker image list
docker image ls

# pip install
docker-compose exec web pip install mysqlclient
docker-compose exec web pip freeze > requirements.txt

# pip install 후 
docker-compose up --build
```
