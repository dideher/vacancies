# Development

### Conda Notes

If you are running a virtual based on conda then after installing
requirements, do the following :

```bash
$ conda install -c anaconda mysqlclient
```

For development a `compose.yml` is offered which covers everything, ie 
a `web` and a `db` component. To bring up the environment simply run :

```bash
$ docker compose up
```

## Migrations

To create django migrations, you need to run the `makemigrations` command
in the `web` container. One simple way to do this :

```bash
$ docker compose exec web python manage.py makemigrations
$ docker compose exec web python manage.py migrate
```

## Superuser

If you need to create a superuser :

```bash
$ docker compose exec web python manage.py createsuperuser
```

# Deployment

## Database


Make sure you have a running MySQL database. If you don't then
you can spawn a docker container with the following :

Create a docker volume :
```commandline
docker volume create mysql-data
```

Create a MySQL instance
```commandline
docker run \
    -e MYSQL_ROOT_USERNAME=root \
    -e MYSQL_ROOT_PASSWORD=root_password \
    -v mysql-data:/var/lib/mysql \
    --name mysql \
    --restart unless-stopped \
    -d \
    mysql:8.0
```

Once the database instance is up & running, connect as a `root`
user and create a database :

```sql
mysql> create database vacancies_db character set utf8;
```

and finally, create the db user

```sql
CREATE USER 'vacancies_user'@'%' IDENTIFIED BY 'XXXXXXXXXX';
GRANT ALL PRIVILEGES ON vacancies_db.* TO 'vacancies_user'@'%';
flush privileges;
```
## Configuration Variables

| Variable               | Description                                  | Example                                                                                             |
|------------------------|----------------------------------------------|-----------------------------------------------------------------------------------------------------|
| ENVIRONMENT            | The active environment                       | DEV                                                                                                 |
| DATABASE_URL           | The database to connect to (LEGACY)          | postgres://username:password@ec2-34-247-118-233.eu-west-1.compute.amazonaws.com:5432/d8feahfemc1tmm |
| DB_HOST                | The database host to connect to              | localhost                                                                                           |
| DB_PORT                | The database port to connect to              | 3306                                                                                                |
| DB_NAME                | The name of the database to use              | db_vacancies                                                                                        |
| DB_USER                | The database user to use when connecting     | db_user                                                                                             |
| DB_PASSWORD            | The database password to use when connecting | db_pass                                                                                             |
| DJANGO_SETTINGS_MODULE | The settings configuration module to use     | vacancies.settings.staging                                                                          |
| EMAIL_HOST             | outgoing email SMTP host                     | smtp-relay.sendinblue.com                                                                           | 
| EMAIL_HOST_PASSWORD    | outgoing email SMTP password                 | XXXYYYYY                                                                                            |
| EMAIL_HOST_USER        | outgoing email SMTP user                     | filippos@slavik.gr                                                                                  |
| SECRET_KEY             | Django's secret key                          | h^(ii@t2snpt=a@n0!c)hqnsedz_2gy%lzgf0vrt23_vx(t675                                                  |
| SENTRY_DSN             | Sentry DNS                                   | https://3c24a0255f07425091a81a493176956f@o521881.ingest.sentry.io/5632525                           |
| SENTRY_ENVIRONMENT     | Sentry Environment                           | staging                                                                                             |

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
    -e ENVIRONMENT=staging \
    -e WEB_CONCURRENCY=4 \
    -e CODE_RELOAD=true \
    -e MAX_REQUESTS=100 \
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

# Django Load & Dump data

Export (dump) data, for example (from heroku) :

```bash
heroku run --app vacancies-dide-next -- python /app/app/manage.py dumpdata --indent 2 --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes > kena-next.json
```

and then to import (load) data run :

```bash
 cat kena-next.json | docker compose exec -T web python manage.py loaddata --format json -
 ```