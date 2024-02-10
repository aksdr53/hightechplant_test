## Tecnhologies
`Python` `Django`  `Docker` `Gunicorn` `NGINX` `PostgreSQL`  

# **_highapp_**
Приложение в котором на данном этапе доступен модуль пользователей, в котором можно зарегестрироваться, просмотреть всех пользователей, посмотреть полную информацию о каждом пользователе, и отредактировать свою информацию.

### Локальный запуск проекта:

**_Склонировать репозиторий к себе_**
```
git@github.com:aksdr53/hightechplant_test.git
```

**_В корневой директории создать файл .env и заполнить своими данными:_**
```
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```

*_Установить Docker, Docker Compose:_**
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```
**_Создать и запустить контейнеры Docker**_
```
sudo docker compose up -d
```
**_Выполнить миграции:_**
```
sudo docker compose exec backend python manage.py migrate
```
**_Собрать статику:_**
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

**_После запуска проект будут доступен по адресу: http://localhost/_**

