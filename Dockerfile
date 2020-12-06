FROM python:3.9-alpine

COPY ./bin/backup_utils.pyz /opt/app/backup-utils

ENV PATH="/opt/app/:$PATH"

CMD ["/opt/app/backup-utils"]
