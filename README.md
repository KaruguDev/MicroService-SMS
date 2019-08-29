# Microservice SMS 

```
This app, queues and sends sms via the set bulk sms aggregators.

Africa's Talking, Twilio and Nexmo have been tested and are working,
this does not mean that you tied to the above three.

Built using Flask

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
1. nano .env
2. add the following parameters:-
    - DATABASE_URL="postgresql://postgres:postgres@localhost/micro_sms"
    - SECRET_KEY="iAmas3cR3Tk3y"
3. save and exit

### Database Migrations
1. flask db init
2. flask db migrate
3. flask db upgrade

### Run Tests
1. python tests.py

### Run Application
1. python manage.py runserver

### Add Bulk SMS providers
1. go to http://127.0.0.1:5000/bulksmsprovider
2. click on "Create"
3. Add the following for Twilio:-
    - Name: twilio
    - API Endpoint: https://api.twilio.com/2010-04-01/Accounts/<Insert Your Account SID>/Messages.json
    - Headers: {'Accept': 'application/json'}
    - Username: <Your Account SID>
    - Password: <Your Account Token>

4. Add the following for Nexmo:-
    - Name: nexmo
    - API Endpoint: https://rest.nexmo.com/sms/json
    - Headers: {'Accept': 'application/json'}

5. Add the following for Africa's Talking:-
    - Name: africas_talking
    - API Endpoint: https://api.africastalking.com/version1/messaging
    - Headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'ApiKey':'<Your generated Aoi Key',
                'Accept':'application/json'
                }

6. You can set any of them as the default, by checking it as default.

### Demo Requests

I will use the python library **requests**, you can use **postman** or **curl** to test

`
import requests

`


