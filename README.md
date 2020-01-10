# Microservice SMS 

```
This Flask app, queues and sends sms via the set bulk sms aggregators.

Africa's Talking, Twilio and Nexmo have been tested and are working,
this does not mean that you are tied to the above three.


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

<<<<<<< HEAD
<<<<<<< HEAD
### Create .env file in the project folder and not in the app folder
=======
### Create .env file
>>>>>>> dda81d8aa21febfe62c13a458a309ade2d3980be
=======
### Create .env file
>>>>>>> dda81d8aa21febfe62c13a458a309ade2d3980be
1. nano .env
2. add the following parameters:-
    - DATABASE_URL="postgresql://postgres:postgres@localhost/micro_sms"
    - SECRET_KEY="iAmas3cR3Tk3y"
    - AFRICAS_TALKING_API_KEY=`<Your AT API KEY>`
    - AFRICAS_TALKING_USERNAME=`<Your AT APP Name>`
<<<<<<< HEAD
<<<<<<< HEAD
    - TWILIO_ACCOUNT_SID = `<Your Twilio Account SID>`
    - TWILIO_ACCOUNT_TOKEN = `<'Your Twilio Account Token>`
    - TWILIO_FROM = `<Twilio Telephone Number>`
    - NEXMO_API_KEY = `<'Your Nexmo API Key>`
    - NEXMO_API_SECRET = `<'Your Nexmo API Secret>`
=======
>>>>>>> dda81d8aa21febfe62c13a458a309ade2d3980be
=======
>>>>>>> dda81d8aa21febfe62c13a458a309ade2d3980be
    - TEST_PHONE=`<Your Mobile Phone Number (254701234567)>`
3. save and exit

### Database Migrations
1. flask db init
2. flask db migrate
3. flask db upgrade

### Run Tests
1. python tests.py

### Run Application
<<<<<<< HEAD
<<<<<<< HEAD
1. export FLASK_ENV='development'
2. flask run
=======
1. python manage.py runserver
>>>>>>> dda81d8aa21febfe62c13a458a309ade2d3980be
=======
1. python manage.py runserver
>>>>>>> dda81d8aa21febfe62c13a458a309ade2d3980be

### Add Bulk SMS providers
1. go to http://127.0.0.1:5000/bulksmsprovider
2. click on "Create"
3. Add the following for Twilio:-
    - Name: twilio
    - API Endpoint: https://api.twilio.com/2010-04-01/Accounts/InsertYourAccountSID/Messages.json
    - Headers: {'Accept': 'application/json'}
    - Username: `<Your Account SID>`
    - Password: `<Your Account Token>`

4. Add the following for Nexmo:-
    - Name: nexmo
    - API Endpoint: https://rest.nexmo.com/sms/json
    - Headers: {'Accept': 'application/json'}

5. Add the following for Africa's Talking:-
    - Name: africas_talking
    - API Endpoint: https://api.africastalking.com/version1/messaging
    - Headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'ApiKey':`<Your generated Api Key>`,
                'Accept':'application/json'
                }

6. You can set any of them as the default, by checking it as default.

### Demo Requests

I will use the python library **requests**, you can use **postman** or **curl** to test

```
import requests
import json

url = "http://127.0.0.1:5000/send-sms/?service="

msg_data = {'to':'254701******, 'message':'Hello, Thanks for using Microservice SMS'}

#Twilio
requests.post(url=url+'twilio', data=json.dumps(msg_data))

#Nexmo
requests.post(url=url+'nexmo', data=json.dumps(msg_data))

#Africas Talking
requests.post(url=url+'africas_talking', data=json.dumps(msg_data))

```

### Delivery Reports
To view your sms delivery reports go to http://127.0.0.1:5000/deliveryreport/

