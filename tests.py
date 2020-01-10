import json
import os
import requests
import time
import unittest
from flask_testing import TestCase, LiveServerTestCase
from app import app, db
from app.config import TestConfig
from app.models import BulkSMSProvider
from app.send_sms import SendSMS

class MicroserviceSMSTest(LiveServerTestCase):
    
    def create_app(self):
        app.config.from_object(TestConfig)
        return app
        
    def  setUp(self):
        db.create_all()

    #Test if the server is running
    def test_1_running_server(self):
        resp = requests.get(self.get_server_url())
        self.assertEqual(resp.status_code, 200)

    #create at bulk sms provider
    def test_2_create_at_bulk_sms_provider(self):
        name = "africas_talking"
        headers = str({'Content-Type': 'application/x-www-form-urlencoded', \
                    'ApiKey': f'{app.config["AFRICAS_TALKING_API_KEY"]}' , 'Accept': 'application/json' })  # database datatype is Text, that is why i am coverting dict to str
    
        api_endpoint = 'https://api.africastalking.com/version1/messaging'

        bsmsp = BulkSMSProvider(name=name, headers=headers, api_endpoint=api_endpoint)
        db.session.add(bsmsp)
        db.session.commit()

        get_bsmp = BulkSMSProvider.query.filter_by(name=name).first()
        self.assertEqual(get_bsmp.name, name)
    
    #create nexmo bulk sms provider
    def test_3_create_nexmo_bulk_sms_provider(self):
        name = "nexmo"
        headers = str({'Accept': 'application/json' })  # database datatype is Text, that is why i am coverting dict to str
        api_endpoint = 'https://rest.nexmo.com/sms/json'

        bsmsp = BulkSMSProvider(name=name, headers=headers, api_endpoint=api_endpoint)
        db.session.add(bsmsp)
        db.session.commit()

        get_bsmp = BulkSMSProvider.query.filter_by(name=name).first()
        self.assertEqual(get_bsmp.name, name)

    #create twilio bulk sms provider
    def test_4_create_twilio_bulk_sms_provider(self):
        name = "twilio"
        headers = str({'Accept': 'application/json' })  # database datatype is Text, that is why i am coverting dict to str
        api_endpoint = f'https://api.twilio.com/2010-04-01/Accounts/{app.config["TWILIO_ACCOUNT_SID"]}/Messages.json'

        bsmsp = BulkSMSProvider(name=name, headers=headers, \
                                api_endpoint=api_endpoint, username=app.config['TWILIO_ACCOUNT_SID'],\
                                password=app.config['TWILIO_ACCOUNT_TOKEN'])
        db.session.add(bsmsp)
        db.session.commit()

        get_bsmp = BulkSMSProvider.query.filter_by(name=name).first()
        self.assertEqual(get_bsmp.name, name)

    #test sending sms with invalid bulk sms provider
    def test_5_send_sms_invalid_bsmsp_and_no_default_bsmp_is_set(self):
        sdata = {'to': f'{app.config["TEST_PHONE"]}', 'message': 'Hello, Tests are being run on Microservice SMS App'}
        send_sms_url = self.get_server_url()+'/send-sms/?service=nexus'

        get_resp = requests.get(url=send_sms_url)
        self.assertEqual(get_resp.status_code, 405)

        post_resp = requests.post(url=send_sms_url, data=sdata)
        time.sleep(2)
    
        self.assertEqual(post_resp.json(), dict(
            error='nexus is not supported yet'))

    #test sending sms with undefined bulks sms provider
    def test_6_send_sms_with_undefined_bsmsp_and_default_bsmp_is_set(self):
        """
            If a bulk sms provider is not defined, the sms can still be sent
            as long as there is a default bulk sms provider
        """
        #set default bsmsp
        name = 'africas_talking'
        bsmp = BulkSMSProvider.query.filter_by(name=name).first()
        bsmp.default = True
        db.session.commit()

        sdata = {'to': f'{app.config["TEST_PHONE"]}', 'message': 'Hello, Tests are being run on Microservice SMS App'}
        send_sms_url = self.get_server_url()+'/send-sms/'

        post_resp = requests.post(url=send_sms_url, data=json.dumps(sdata))
        time.sleep(2)

        self.assertIn(post_resp.status_code, [201])
        self.assertDictContainsSubset({'bulk_sms_provider': 'africas_talking'}, post_resp.json())
    
    #test sending sms with a valid bulk sms provider
    def test_7_send_sms_with_no_data(self):
        send_sms_url = self.get_server_url()+'/send-sms/?service=africas_talking'

        post_resp = requests.post(url=send_sms_url)
        time.sleep(2)

        self.assertEqual(post_resp.json(), {'error':'No data was passed'})

    #test sending sms with a valid bulk sms provider
    def test_8_send_sms_with_missing_data(self):
        send_sms_url = self.get_server_url()+'/send-sms/?service=africas_talking'

        sdata = {'message': 'Hello, Tests are being run on Microservice SMS App'}
        post_resp = requests.post(url=send_sms_url, data=json.dumps(sdata))
        time.sleep(2)
    
        self.assertEqual(post_resp.json(), {'error':'No sender'})

    
    #test sending sms with a valid bulk sms provider
    def test_9_send_sms_valid_via_at(self):
        sdata = {'to': f'{app.config["TEST_PHONE"]}', 'message': 'Hello, Tests are being run on Microservice SMS App'}

        send_sms_url = self.get_server_url()+'/send-sms/?service=africas_talking'

        post_resp = requests.post(url=send_sms_url, data=json.dumps(sdata))
        time.sleep(2)
    
        self.assertIn(post_resp.status_code, [201])
        self.assertDictContainsSubset({'bulk_sms_provider': 'africas_talking'}, post_resp.json())
    
    
    #test sending sms with a valid bulk sms provider
    def test_10_send_sms_valid_via_twilio(self):
        sdata = {'to': f'{app.config["TEST_PHONE"]}', 'message': 'Hello, Tests are being run on Microservice SMS App'}

        send_sms_url = self.get_server_url()+'/send-sms/?service=twilio'

        post_resp = requests.post(url=send_sms_url, data=json.dumps(sdata))
        time.sleep(2)
        
        self.assertIn(post_resp.status_code, [200, 201, 202])
        self.assertDictContainsSubset({'bulk_sms_provider': 'twilio'}, post_resp.json())

    
    #test sending sms with a valid bulk sms provider
    def test_11_send_sms_valid_via_nexmo(self):
        sdata = {'to': f'{app.config["TEST_PHONE"]}', 'message': 'Hello, Tests are being run on Microservice SMS App'}

        send_sms_url = self.get_server_url()+'/send-sms/?service=nexmo'

        post_resp = requests.post(url=send_sms_url, data=json.dumps(sdata))
        self.assertDictContainsSubset({'bulk_sms_provider': 'nexmo'}, post_resp.json())

    #destory database last
    def test_12_destroy_database(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
