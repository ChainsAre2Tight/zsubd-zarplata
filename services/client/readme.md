# подключение
> docker exec -it postgres-client /bin/bash
## ssh
> ssh root@postgres-server
### пароль: 
> root

# ssh port forwarding
> ssh -L 5432:localhost:5432 postgres-server
# тест
> psql -h localhost -d zarplata