FROM python:3.9
# 파이썬에서 출력 버퍼가 기본으로 작동하면서 출력 로그를 붙잡고 있기 때문에 로그가 한 발 늦게 출력된다.
# 이 버퍼링을 없애려면 아래 환경변수를 추가하면 된다.
ENV PYTHONUNBUFFERED 0
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
# 개발용에서는 소스코드를 컨테이너에 넣을 필요가 없다
# 앱 코드: 앱 코드는 컨테이너 안에 집어 넣지 않고 로컬 컴퓨터의 디렉터리를 참조
# COPY . /app/
EXPOSE 8000
# 데이터베이스 서비스가 실행된 후 초기화되기 전에 Django 서버가 실행되기 때문에 django 서버가 DB를 못찾음
# wait-for-it.sh이라는 셸 스크립트를 사용 - 특정 서버의 특정 포트로 접근할 수 있을 때까지 기다려주는 스크립트
ADD    https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN chmod +x /wait-for-it.sh
CMD [ "./wait-for-it.sh" ]