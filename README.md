## Job Portal

### Установка

```
pip install -r requirements.txt
```

###  Миграция и загрузка в базу данных о суперпользователе
```sh
docker-compose exec web python manage.py makemigrations
```
```sh
docker-compose exec web python manage.py migrate --noinput
```
```sh
docker-compose exec web manage.py loaddata db.json
```