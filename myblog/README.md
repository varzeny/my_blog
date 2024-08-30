# my_blog

## env
django, daphne, mysql, nginx

## install
you must remake .env

## activate




### 직접제어시
#### 프로젝트에 .env 만들것
#### 컨테이너
sudo docker run -d --name container-myblog-240829 \
  -v ~/prj/myblog/myblog:/app \
  varzeny/myblog-240829

#### nginx



### 자동배포시
#### 컨테이너
sudo docker run -d --name container-myblog-240829 \
  -v ~/app/myblog/staticfiles:/app/staticfiles \
  -v ~/app/myblog/media:/app/media \
  varzeny/myblog-240829

#### nginx
server {
    listen 80;
    server_name varzeny.com www.varzeny.com;

    # HTTP 요청을 HTTPS로 리디렉션
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name varzeny.com www.varzeny.com;

    # SSL 인증서 설정
    ssl_certificate /etc/letsencrypt/live/varzeny.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/varzeny.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # 정적파일 서빙
    location /static/ {
        alias /home/ubuntu/app/myblog/staticfiles/;
    }

    # 미디어 파일 서빙
    location /media/ {
        alias /home/ubuntu/app/myblog/media/;
    }
    location / {
        proxy_pass http://myblog_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 지원
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

upstream myblog_backend {
    server 172.17.0.2:9000 max_fails=3 fail_timeout=30s;  # Daphne 인스턴스 1
}



### local
daphne -b 0.0.0.0 -p 9000 myblog.asgi:application
