# Установка:
> git clone https://github.com/ChainsAre2Tight/zsubd-zarplata
# Обновление:
> git fetch & git pull
# Первый запуск (или после обновления):
> (sudo) docker-compose build
# Запуск:
> (sudo) docker-compose up -d
# Подключение:
> (sudo) docker-compose attach postgres-client
# Проверка работы:
> select version();
# Выход:
> exit
# Выключение:
> (sudo) docker-compose down