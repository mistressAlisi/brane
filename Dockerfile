FROM debian:trixie
RUN  apt-get update;



RUN  apt install -y postgresql-common;
RUN  /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y;

RUN apt-get install --no-install-recommends -y \
    openssl \
    build-essential \
    curl \
    xz-utils \
    ca-certificates \
    fontconfig \
    python3.13 \
    python3.13-venv \
    python-is-python3 \
    libpq-dev \
    python3.13-dev \
    uwsgi-plugin-python3 \
    uwsgi-emperor \
    uwsgi-plugin-alarm-xmpp \
    uwsgi-plugin-emperor-pg \
    uwsgi-plugin-geoip \
    uwsgi \
    nginx \
    rabbitmq-server \
    postgresql-client-17;


WORKDIR /
ADD ./devops/container_fs/etc /etc
ADD ./devops/container_fs/usr /usr
ADD ./devops/container_fs/root /root
#COPY ./devops/container_fs/* /
WORKDIR /app
ADD requirements.txt /app/requirements.txt
#COPY ./devops/container_fs/etc/banner /etc/banner/
RUN set -ex \
    && apt-get -y install libgmp-dev \
    && python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r /app/requirements.txt;

RUN apt-get clean




ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

EXPOSE 8000
ADD ./brane /app/brane
RUN python3 /app/brane/manage.py collectstatic --noinput
RUN rm -rf /etc/uwsgi/apps-enabled/*
RUN rm -rf /etc/nginx/sites-enabled/*
RUN mkdir -p /run/uwsgi/
RUN chown -R www-data:www-data /run/uwsgi
RUN ln -s /etc/uwsgi/apps-available/brane.ini /etc/uwsgi/apps-enabled
RUN ln -s /etc/nginx/sites-available/*.conf /etc/nginx/sites-enabled/
CMD ["bash", "/usr/bin/docker_entry.sh"]
