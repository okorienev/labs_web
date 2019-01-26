FROM python:3.6-alpine


ENV UPLOADS_PATH=/uploads
ENV DOCS_FOLDER=course_docs
ENV SNAPSHOT_FOLDER=snapshots
RUN mkdir -p  $UPLOADS_PATH
WORKDIR $UPLOADS_PATH
RUN mkdir -p $DOCS_FOLDER
RUN mkdir -p $SNAPSHOT_FOLDER


ENV INSTALL_PATH=/labs_web
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY requirements.txt requirements.txt


RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .


CMD gunicorn -b 0.0.0.0:8000 -access-logfile -"labs_web.runserver"


