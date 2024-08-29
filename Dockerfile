# 1. Python 3.10-slim 베이스 이미지 사용
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. requirements.txt 파일만 복사
COPY requirements.txt .

# 4. 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 파일을 복사
COPY . /app

# 6. 명령어 설정 (Daphne 실행)
CMD ["daphne", "-b", "0.0.0.0", "-p", "9000", "myblog.myblog.asgi:application"]
