FROM ubuntu:latest

COPY . /app
COPY ./firebase-web-api.key /app
COPY ./run.py /app

WORKDIR /app

RUN apt-get update
RUN apt-get install python3 python3-pip python3-dev -y
RUN pip install -r requirements.txt --no-input

# Timezone
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN useradd -ms /bin/bash cc-api -u 1000
USER cc-api

CMD ["python3", "run.py"]