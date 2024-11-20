FROM postgres:17rc1

WORKDIR /usr/src

# copy entrypoint files
COPY ./init.sql /docker-entrypoint-initdb.d/

# install ssh server
RUN apt update -y && apt install -y openssh-server

# start ssh server
# RUN "/etc/init.d/ssh start"