### хз как сделать автостарт ссш сервера...

# после запуска контейнера
> docker exec -it postgres-server /bin/bash
# в нем
> service ssh start

# ssl certificate
cd /var/lib/postgresql

openssl req -new -x509 -days 365 -nodes -text -out server.crt \
  -keyout server.key -subj "/CN=root"

openssl req -new -nodes -text -out root.csr \
  -keyout root.key -subj "/CN=root"
chmod og-rwx root.key

openssl x509 -req -in root.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey root.key -out root.crt

openssl req -new -nodes -text -out server.csr \
  -keyout server.key -subj "/CN=postgres-server"
chmod og-rwx server.key

openssl x509 -req -in server.csr -text -days 365 \
  -CA root.crt -CAkey root.key -CAcreateserial \
  -out server.crt



openssl req -new -nodes -text -out postgresql.csr \
  -keyout postgresql.key -subj "/CN=admin"
chmod og-rwx postgresql.key

openssl x509 -req -in postgresql.csr -text -days 365 \
  -CA root.crt -CAkey root.key -CAcreateserial \
  -out postgresql.crt