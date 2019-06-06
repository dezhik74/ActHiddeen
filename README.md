# Правила развертывания ActHiddeen

пароль амд БД 123

имя пользователя БД из джанго user2 -> pww2

название базы данных django_db
***
Ubuntu Server 16.04 + Django + Python3 + Nginx + Gunicorn

Корневая папка

/home/user/ActHiddeen/

Папка проекта (там файл manage.py)

/home/user/ActHiddeen/app/acts
***
#### 1) Для начала нужно сделать апгрейд
```
sudo apt-get update
sudo apt-get upgrade
```
#### 2) Python3.5 уже стоит в ubuntu server 16.04

#### 3) Поставим nginx
```
sudo apt-get install nginx
```
#### 4) Ставим третий pip.
```
sudo apt-get install python3-setuptools
sudo easy_install3 pip
```
#### 5) Virtualenv
установим само виртуальное окружение
```
pip3 install virtualenv #если pip не хочет, можете поставить командой easy_install3 virtualenv
```
в корневой папке
```
virtualenv /venv   # venv можете заменить на любое другое имя
source /venv/bin/activate
```
деактивация deactivate

#### 6) Ставим gunicorn. 
*** !!!! В VENV используем pip, вне VENV используем pip3 ***
```
pip install gunicorn
```
#### 7) Клонируем из github. на уровне выше корневой папки 
```
git clone https://github.com/dezhik74/ActHiddeen.git
```
#### 8) Устанавливаем все пакеты проекта.
```
(venv)$  pip install -r 'requirements.txt'
```
#### 9) Решение проблемы статики в gunicorn.
```
nano settings.py
```
прописываем 
```
STATIC_ROOT = '/home/user/ActHiddeen/static/' - если в корневой хотим
```
в папке проекта
```
python manage.py collectstatic
```
там появится папка /static/

#### 10) Настройка ngnix
```
cd /etc/nginx/sites-available/
nano default
```
Удаляем оттуда все и пишем

```
server {
    listen 80;
    server_name 111.222.333.44; #либо ip, либо доменное имя
    access_log  /var/log/nginx/example.log;

    location /static/ {
        root /opt/myenv/myproject/;
        expires 30d;
    }
    location / {
        proxy_pass http://127.0.0.1:8000; 
        proxy_set_header Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
##### перезапуск ngnix
```
sudo service nginx restart
```
##### запуск gunicorn
в папке проекта
```
gunicorn acts.wsgi:application
```
#### 11) Ставим сам сервер PostgreSQL и библиотеку разработчика (она пригодится нам при установке бэкэнда)
```
sudo apt-get install postgresql postgresql-server-dev-9.5
```
#### 12) Открываем консоль PostgreSQL
```
sudo -u postgres psql postgres
```
#### 13) Задаем пароль администратора БД
```
\password postgres
```
#### 14) Создаем и настраиваем пользователя при помощи которого будем соединяться с базой данных из Django. 
Заодно указываем значения по умолчанию для кодировки, уровня изоляции транзакций и временного пояса
```
create user user_name with password 'password';
alter role user_name set client_encoding to 'utf8';
alter role user_name set default_transaction_isolation to 'read committed';
alter role user_name set timezone to 'UTC'; (берется из settings.py)
```
#### 15) Создаем базу для нашего проекта
```
create database django_db owner user_name;
```
#### 16) Выходим из консоли
```
\q
```
#### 17) В окружении проекта устанавливаем бэкэнд для PostgreSQL
```
pip install psycopg2    (в системе должен быть установлен компилятор си)
```
#### 18) Последний наш шаг - настроить раздел DATABASES конфигурационного файла проекта settings.py

```
DATABASES = {
	'default': {
	
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'django_db',
		'USER' : 'user_name',
		'PASSWORD' : 'password',
		'HOST' : '127.0.0.1',
		'PORT' : '5432',
    }
}
```

#### 19) создание дампа базы / использование дампа базы
в папке проекта
```
python manage.py dumpdata --indent=2 --exclude=contenttypes > datadump.json
```
обратно
```
python manage.py loaddata datadump.json
```

### Ссылки на руководоства

[Django+PostgreSQL за 8 шагов](https://djbook.ru/examples/77/)

[Django + Python3 + Nginx + Gunicorn + DO](https://djbook.ru/examples/62/)

[Инструкция: как перевести проект Django с SQLite на MySQL без боли](https://tproger.ru/articles/django-sqlite-to-mysql/)

[Python+gunicorne+posgressql+nginx -> Docker](https://www.haikson.com/programmirovanie/python/django-nginx-gunicorn-postgresql-docker/)

[Хороший учебник по докеру](https://habr.com/ru/post/310460/)

Номер 2 19.03 7.5
Номер 1 02. 42250
Номер 1 03. 99980.55
Номер 1 04. 20434

 
 
 
