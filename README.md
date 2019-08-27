# Microservice SMS 

```
This app, queues and sends sms via the bulk sms providers' HTTP endpoints to the respective recepients

```

### Create virtualenv
1. cd <virtual_env_folder>
2. virtualenv -p python3 micro_sms_env
3. source micro_sms_env/bin/activate
4. cd <project_folder>
5. pip install -r requirements.txt

### Create Database
1. sudo su - postgres
2. psql
3. CREATE DATABASE micro_sms;
4. \q
5. exit

### Create .env file
1. cp .env.copy .env
2. 

### Database Migrations
1. flask db init
2. flask db migrate
3. flask db upgrade

### Run Application
1. python manage.py runserver

### Add Bulk SMS providers

### Demo Requests