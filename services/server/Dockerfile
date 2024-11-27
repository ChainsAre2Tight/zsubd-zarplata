FROM postgres:17rc1

WORKDIR /usr/src

# change password root
RUN echo "root:root" | chpasswd

# install ssh server
RUN apt update -y && apt install -y openssh-server

# enable root login
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# copy entrypoint files
COPY ./init.sql /docker-entrypoint-initdb.d/