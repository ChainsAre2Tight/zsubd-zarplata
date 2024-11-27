FROM ubuntu:22.04

WORKDIR /psql-client

# install psql
RUN apt update -y 

# install nmap
RUN apt install -y nmap

# install ssh client
RUN apt install -y openssh-client

RUN apt install -y wget gnupg
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt update -y
RUN apt install -y postgresql-client-17
