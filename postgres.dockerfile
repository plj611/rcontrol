FROM postgres:12.3
ENV POSTGRES_PASSWORD helloworld123

COPY initdb.sql /docker-entrypoint-initdb.d/initdb.sql
