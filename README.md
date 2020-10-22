# XMP Backend

## Setup

### Clone

```
$ git clone git@github.com:numbersprotocol/xmp-backend.git
$ cd xmp-backend
```

### Create .env file for secret variables

```
$ cp xmp_backend/.env.example xmp_backend/.env
# Edit xmp_backend/.env
```

All example variables are required. Note that the `.env` file must be located in the same folder as `manage.py`.

#### .env settings

##### DEBUG

Always set to `False` if deploying for production.

##### USE_SSL

Set to `True` if SSL is used.

##### SECRET_KEY

A unique key for cryptographic signature used in Django App. Can be generated by

```
$ python3
>>> from django.core.management.utils import get_random_secret_key  
>>> get_random_secret_key()
```

##### HOST_NAME

The server's host name.

##### DJANGO_SU_NAME/DJANGO_SU_PASSWORD

When migrating the database (which is done in Docker building), a superuser will be created. The user's credentials could be used to retrieve login token from `/auth/token/login/` API endpoint.

The step is required since user registration is disabled.

Password has 8 character minimal length restriction.

##### EXTERNAL_API_ENDPOINT/EXTERNAL_API_KEY

`EXTERNAL_API_ENDPOINT` is the the full API url for the "Get Signed Url" API. `EXTERNAL_API_KEY` is self-explanatory.


### Docker

```
$ docker build -t xmp_backend:v1 .
$ docker run -p 8000:8000 --network host xmp_backend:v1
```

Now the application is alive and listens to localhost:8000.

Setup a reverse proxy server (Nginx is recommended). Refer to `xmp_backend_nginx.conf.example` for Nginx site conf example.

### Dev Server

Note: Only use Dev server mode for development since it has security and performance concerns.

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements.txt
(venv)$ cd xmp_backend
(venv)$ python3 manage.py migrate
(venv)$ python3 manage.py runserver
```

## Usage

The API doc could be viewed from visiting `<host-url>/redoc` or `<host-url>/swagger`.

There are 3 APIs: `/auth/token/login/`, `/auth/token/logout/` and `/injection/`.

### /auth/token/login/

Use the username and password defined in `.env` to retrieve the login token.

### /auth/token/logout/

Authentication header required. Expires the login token.

### /injection/

Authentication header required. See the API doc for details.
