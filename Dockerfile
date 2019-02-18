FROM python:3.6-alpine


ENV INSTALL_PATH=/labs_web
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY requirements.txt requirements.txt

ENV UPLOADS_PATH=$INSTALL_PATH/labs_web/uploads
ENV DOCS_FOLDER=course_docs
ENV SNAPSHOT_FOLDER=snapshots
ENV TEST_DATA=$INSTALL_PATH/labs_web/test_data

RUN mkdir -p  $UPLOADS_PATH
RUN mkdir -p $UPLOADS_PATH/$DOCS_FOLDER
RUN mkdir -p $UPLOADS_PATH/$SNAPSHOT_FOLDER


RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .


CMD gunicorn -b 0.0.0.0:8000 -access-logfile -"labs_web.runserver"


