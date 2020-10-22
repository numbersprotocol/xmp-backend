FROM python:3.8-alpine

RUN apk update && apk add jpeg-dev zlib-dev exiv2-dev boost-dev boost-python3
RUN apk update && apk add --virtual .build-deps git gcc g++

RUN mkdir -p /usr/src/xmp_backend
WORKDIR /usr/src/xmp_backend
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apk del .build-deps

EXPOSE 8000

WORKDIR /usr/src/xmp_backend/xmp_backend
RUN python3 manage.py migrate

CMD ["gunicorn", "xmp_backend.wsgi", "0:8000", "--log-level=info", "--access-logfile", "-", "--enable-stdio-inheritance", "--workers", "4"]
