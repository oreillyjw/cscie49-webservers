FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN apk --no-cache add --virtual build-dependencies \
      build-base \
      py-mysqldb \
      gcc \
      libc-dev \
      libffi-dev \
      mariadb-dev \
      && pip install -qq -r requirements.txt \
      && rm -rf .cache/pip \
      && apk del build-dependencies

RUN apk -q --no-cache add mariadb-client-libs
RUN pip install -r requirements.txt
RUN pip install -U gunicorn
# RUN apk add bash
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "homepage:homepage"]
