# pull the official base image
FROM --platform=linux/amd64 python:3.8.3-alpine

# set work directory
WORKDIR /app


# install dependencies
RUN pip install --upgrade pip
RUN apk update
RUN apk add git
RUN apk add gcc musl-dev mariadb-connector-c-dev libffi-dev make
RUN apk --update add libxml2-dev libxslt-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# copy project
COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
