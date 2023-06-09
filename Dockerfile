# pull the official base image
FROM python:3.10.2-slim-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./plugins.txt /usr/src/app
RUN pip install --no-cache-dir -r plugins.txt --use-deprecated=legacy-resolver
# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]