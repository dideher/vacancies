
## Docker Info

Create a Docker network for the app
```commandline
docker network create vacancies-net
```

Attach the running mysql container to the application's network (assume the mysql container is called `mysql`)

```commandline
docker network connect --alias mysql vacancies-net mysql
```
```commandline
docker build . -t dideira/vacancies-web:latest
```

```commandline
docker run --rm -it --name vacancies \
    -e DJANGO_SETTINGS_MODULE=vacancies.settings.staging \
    -e DB_NAME=vacancies_db \
    -e DB_USER=vacancies \
    -e DB_PASS=vacancies \
    -e DB_HOST=mysql \
    -e DB_PORT=3306 \
    -e VIRTUAL_HOST=vacancies-dev.dide.ira.net \
    --network vacancies-net \
    dideira/vacancies-web:latest
```

or for local development

```commandline
docker run --rm -it --name vacancies \
    -e DJANGO_SETTINGS_MODULE=vacancies.settings.docker-dev \
    -p 8000:80 \
    dideira/vacancies-web:latest
```

or daemonize it
```commandline
docker run --name vacancies \
    -e DJANGO_SETTINGS_MODULE=vacancies.settings.staging \
    -e DB_NAME=vacancies_db \
    -e DB_USER=vacancies \
    -e DB_PASS=vacancies \
    -e DB_HOST=mysql \
    -e DB_PORT=3306 \
    -e VIRTUAL_HOST=vacancies-dev.dide.ira.net \
    -d \
    --network vacancies-net \
    --restart unless-stopped \
    dideira/vacancies-web:latest
```

# Nginx Proxy

In case you need a nginx proxy, then you may

```commandline
docker network create nginx-proxy
```

```commandline
docker run -d -p 80:80 --restart unless-stopped \
    --name nginx-proxy \
    -v /var/run/docker.sock:/tmp/docker.sock:ro \
    --net nginx-proxy \
    jwilder/nginx-proxy
```

Don't forget to add the nginx-proxy container to the `vacancies-net` network
```commandline
docker network connect vacancies-net nginx-proxy
```