FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip3 install --upgrade pip

ENV APP_DIR /deploy

RUN mkdir -p ${APP_DIR}

COPY . ${APP_DIR}

WORKDIR ${APP_DIR}

RUN pip3 install -r ${APP_DIR}/requirements.txt

EXPOSE 5001

CMD ["gunicorn",  "app:app", "-b", "0.0.0.0:5001", "-w", "4"]
