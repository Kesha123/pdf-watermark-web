FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget unzip && \
    apt-get clean

RUN wget https://github.com/pocketbase/pocketbase/releases/download/v0.22.19/pocketbase_0.22.19_linux_amd64.zip -O /tmp/pocketbase.zip

RUN unzip /tmp/pocketbase.zip -d /usr/local/bin && \
    rm /tmp/pocketbase.zip

COPY . /usr/local/bin/

RUN chmod +x /usr/local/bin/pocketbase

EXPOSE 8090

WORKDIR /usr/local/bin

ENTRYPOINT ["pocketbase", "serve", "--http=0.0.0.0:8090"]
