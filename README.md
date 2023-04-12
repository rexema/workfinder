## Job Portal

### Установка

```
pip install -r requirements.txt
```

### Запуск
```sh
docker-compose up -d
```

Что бы docker-compose запускать без sudo нужно сделать следующее:
```
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
```

### Первичные действия
Проводим миграцию и вносим данные о суперпольщователе. Хотя можно создать своего с помощью createsuperuser

```sh
docker-compose exec web python manage.py migrate
```
```sh
docker-compose exec web python manage.py loaddata db.json
```
### Админ-панель
```
login: admin@email.com
passw: 123
```

http://127.0.0.1:8000