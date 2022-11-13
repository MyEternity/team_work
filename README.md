## Проект "Крабр круче, чем Хабр!"
## Командная разработка по методологии Agile:Scrum
## Сайт для обучения

### Базовая документация к проекту

Основные системные требования:

* Ubuntu 20.04 LTS
* Python 3.9
* Django 4.1
* Зависимости (Python) из requirements.txt

### Установка необходимого ПО
#### Обновляем информацию о репозиториях
```
apt update
```
#### Установка nginx, Git, virtualenv, gunicorn
```
apt install nginx
```
Git
```
apt install git-core
```
virtualenv
```
apt install python3-venv
```
gunicorn
```
apt install gunicorn
```
#### Настраиваем виртуальное окружение
При необходимости, для установки менеджера пакетов pip выполняем команду:
```
apt install python3-pip
```
Создаем и активируем виртуальное окружение:
```
mkdir /opt/venv
python3 -m venv /opt/venv/team_work_env
source /opt/venv/team_work_env/bin/activate
```
Создаем директории под логи:
```
mkdir /opt/venv/team_work_env/run/
mkdir /opt/venv/team_work_env/logs/
mkdir /opt/venv/team_work_env/logs/nginx/
```
Устанавливаем права:
```
chown -R hh /opt/venv/team_work_env
```
Клонируем репозиторий:
```
git clone https://github.com/GeekbrainsProject/team_work.git /opt/venv/team_work_env/src
cd team_work_env/
```
Ставим зависимости:
```
pip3 install -r /opt/venv/team_work_env/src/team_work/requirements.txt
```
#### Суперпользователь
```
python3 manage.py createsuperuser
```
к примеру (логин/пароль): admin:admin
#### Выполнение миграций и сбор статических файлов проекта
Выполняем миграции:
```
python3 manage.py migrate
```
Собираем статику:
```
python3 manage.py collectstatic
```
#### Заполнить базу данных тестовыми данными (не обязательно)
```
python3 manage.py fill_db
```
#### Тест запуска
```
python3 manage.py runserver
```
#### Назначение прав доступа
```
chown -R xabr /home/team_work_env/
chmod -R 755 /home/team_work_env/team_work/
```
Настроим параметры службы «gunicorn»
```
sudo nano /etc/systemd/system/gunicorn.service


[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=USER_NAME
Group=www-data
WorkingDirectory=/home/team_work_env/team_work
ExecStart=/home/team_work_env/team_work/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/team_work_env/team_work/team_work.sock xabr.wsgi

[Install]
WantedBy=multi-user.target

```
Активирование и запуск сервиса
```
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```
Настройки параметров для nginx
```
sudo nano /etc/nginx/sites-available/team_work.conf

server {
    listen 80;
    server_name 151.248.117.226; ### server_name необхоимо написать ip-адрес сервера

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/team_work_env/team_work;
    }

    location /media/ {
        root /home/team_work_env/team_work;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/team_work/team_work/team_work.sock;
    }
}
```
Перезапускаем службу «nginx»
```
sudo systemctl restart nginx
```
#### Активировируем сайт
```
sudo ln -s /etc/nginx/sites-available/team_work /etc/nginx/sites-enabled
```

### После этого в браузере можно ввести ip-адрес сервера и откроется проект.
#### Выкат изменений из Git:
```
source /opt/venv/team_work/bin/activate
cd /opt/venv/team_work/src
git pull origin master
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic