FROM python:3.7-alpine

# run in unbuffered mode which is recommended when running Python
# The reason for this is that it doesn't allow Python to buffer the outputs.
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# creates a user the '-D' says create a user, going to be used for 
# running applications only.
RUN adduser -D user
USER user
