FROM mariadb:10.3.9
COPY . /http-exec
RUN apt update && apt install -y runit python3 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /supervisor/mysqld && echo '#!/bin/sh\n/docker-entrypoint.sh mysqld' > /supervisor/mysqld/run \
    && chmod a+x /supervisor/mysqld/run \
    && mkdir -p /supervisor/serv && ln -s /http-exec/http-exec.py /supervisor/serv/run \
    && chown -R mysql:mysql /supervisor
EXPOSE 8000
USER mysql
ENTRYPOINT ["/usr/bin/runsvdir", "-P", "/supervisor"]
