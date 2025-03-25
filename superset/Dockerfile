FROM apache/superset:latest

USER root
RUN  apt-get update && apt-get install -y default-libmysqlclient-dev && pip install mysqlclient


RUN pip install pinotdb

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY ./superset-init.sh /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT ["/superset-init.sh"]