FROM python:2.7
ARG JSON_PATH=/tmp/cache/json.data
ENV JSON_PATH $JSON_PATH
ARG SECOND_MASTER=localhost
ENV SECOND_MASTER $SECOND_MASTER
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
