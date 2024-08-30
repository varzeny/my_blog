# 1. Python 3.10-slim 베이스 이미지 사용
FROM python:3.10-slim

# 2. 시스템 패키지 설치 (mysqlclient 관련 패키지 포함)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. requirements.txt 파일 복사
COPY requirements.txt .

# 5. 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 개발환경에서 직접 호스트 파일을 참조시에는 필요 없음
# 6. 나머지 프로젝트 파일 복사
# COPY . /app

# 7. (선택 사항) Static 파일 수집
# RUN python manage.py collectstatic --noinput


# 8. 명령어 설정 (Daphne 실행)
CMD ["sh", "-c", "python manage.py makemigrations  && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \
daphne -b 0.0.0.0 -p 9000 myblog.asgi:application"]




# CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 9000 myblog.asgi:application"]
