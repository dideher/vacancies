FROM python:3.8-alpine AS compile-image
ARG ENVIRONMENT=development
ENV SU_EXEC_VERSION 0.2

## update alpine and install build deps
RUN set -x \
    apk update \
    && apk add --no-cache \
        gcc \
        libc-dev \
        linux-headers \
        jpeg-dev \ 
        zlib-dev \
        libjpeg  \
        mariadb-dev
        #mariadb-client
        #postgresql-dev

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## install requirements
RUN set -x \
    && pip install --upgrade pip wheel pip-tools

COPY requirements.txt ./requirements.in

## update requirements file with deployment requirement deps
RUN echo "gunicorn" >> /requirements.in
RUN echo "meinheld" >> /requirements.in
RUN echo "mysqlclient" >> /requirements.in

RUN set -x \
    && pip-compile ./requirements.in > ./requirements.txt \
    && pip-sync \
    && pip install -r ./requirements.txt


FROM python:3.8-alpine AS runtime-image
ARG ENVIRONMENT=development

# partially inspired from https://github.com/tiangolo/meinheld-gunicorn-docker

## update alpine and install runtime deps
RUN set -x \
    apk update \
    && apk add --virtual \
        libjpeg-turbo \ 
        zlib \
        libjpeg \
        openssl \
        ca-certificates \
        mariadb-connector-c

## copy Python dependencies from build image
COPY --from=compile-image /opt/venv /opt/venv

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./app /app
WORKDIR /app/


ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Meinheld
CMD ["/start.sh"]

# FROM python-base:latest

# ENV PATH="/vacancies/_docker/scripts:${PATH}"

# RUN mkdir /vacancies
# COPY . /vacancies
# WORKDIR /vacancies

# RUN chmod +x /vacancies/_docker/scripts/*

# RUN mkdir -p /vol/web/media

# RUN adduser -D user
# RUN chown -R user:user /vol
# RUN chown -R user:user /vacancies
# RUN chmod -R 755 /vol/web
# USER user

# CMD ["entrypoint.sh"]
