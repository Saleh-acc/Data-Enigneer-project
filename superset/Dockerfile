FROM apache/superset:latest

USER root

RUN #apt-get update && apt-get install -y default-libmysqlclient-dev && pip install mysqlclient
RUN pip install pinotdb

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

# Copy the superset-init.sh script and fix line endings + permissions
COPY ./superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh
#RUN sed -i 's/\r$//' /superset-init.sh && chmod +x /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT ["/superset-init.sh"]