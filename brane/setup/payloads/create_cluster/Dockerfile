
FROM docker.io/library/postgres:17.5-bookworm
ARG PGUSER=brane
ARG PGUSER_PASSWD=password
WORKDIR /
RUN mkdir -p docker-entrypoint-initdb.d
ADD ./postgres_fs/docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/

RUN export SED_PGUSER=$PGUSER && \
    export SED_PGUSER_PASSWD=$PGUSER_PASSWD \
    && sed -i "s/{PGUSER}/${SED_PGUSER}/g" /docker-entrypoint-initdb.d/*.sql \
    && sed -i "s/{PGUSER_PASSWD}/${SED_PGUSER_PASSWD}/g" /docker-entrypoint-initdb.d/*.sql && \
    unset SED_PGUSER && unset SED_PGUSER_PASSWD

