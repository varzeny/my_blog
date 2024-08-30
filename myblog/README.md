# my_blog

## env
django, daphne, mysql, nginx

## install
you must remake .env

## activate

### docker container
sudo docker run -d --name container-myblog-240829 \
  -v ~/app/myblog/staticfiles:/app/staticfiles \
  -v ~/app/myblog/media:/app/media \
  varzeny/myblog-240829

### local
daphne -b 0.0.0.0 -p 9000 myblog.asgi:application
