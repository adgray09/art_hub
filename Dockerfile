# STEP 1

FROM python:3.7-slim-buster

# STEP 2

ADD . /todo

# STEP 3

WORKDIR /todo

# STEP 4

RUN pip install -r requirements.txt

