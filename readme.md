# Установка:
> git clone https://github.com/ChainsAre2Tight/zsubd-zarplata
# Обновление:
> git pull
## Первый запуск (или после обновления):
> (sudo) docker-compose build
# Запуск:
> (sudo) docker-compose up -d
## Подключение:
> (sudo) docker-compose attach postgres-client
## Проверка работы:
> select version();
## Выход:
> exit
## Выключение:
> (sudo) docker-compose down

## альтернативное подключение
### Для Windows:
> ./scripts/connect.bat
### Для Linux:
> source ./scripts/connect.sh

## Создание таблиц
### Для Windows:
> ./scripts/create-db.bat;
### Для Linux:
> source ./scripts/create-db.sh

## Заполнение таблиц
### Для Windows:
> ./scripts/seed.bat
### Для Linux:
> source ./scripts/seed.sh