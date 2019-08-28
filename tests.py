from flask_testing import TestCase, LiveServerTestCase
import json
import requests
import unittest
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

    #create bulk sms provider
    def test_2_create_bulk_sms_provider(self):
        name = "twilio"
        headers = str({'Accept': 'application/json'}) #database datatype is Text, that is why i am coverting dict to str
        api_endpoint = 'https://api.twilio.com/2010-04-01/Accounts/AC9d603f2a0e7eb8b421d4fd968f7bad9d/Messages.json'
        username = 'AC9d603f2a0e7eb8b421d4fd968f7bad9d'
        password = '4294c80514d961d1bb3aea8c007b7d44'

        bsmsp = BulkSMSProvider(name=name, headers=headers, api_endpoint=api_endpoint, username=username, password=password)
        db.session.add(bsmsp)
        db.session.commit()

        get_bsmp = BulkSMSProvider.query.filter_by(name=name).first()
        self.assertEqual(get_bsmp.name, name)

    #test sending sms with invalid bulk sms provider
    def test_3_send_sms_invalid_bsmsp(self):
        sdata = {'To': '+254720905558', 'From': '+19386669155',
                'Body': 'Hello, Tests are being run on Microservice SMS App'}

        send_sms_url = self.get_server_url()+'/send-sms/?service=twilo'

        get_resp = requests.get(url=send_sms_url)
        self.assertEqual(get_resp.status_code, 405)

        post_resp = requests.post(url=send_sms_url, data=sdata)
    
        self.assertEqual(post_resp.json(), dict(
            error='Bulk SMS Provider has not been defined'))

    #test sending sms with undefined bulks sms provider
    def test_4_send_sms_with_undefined_bsmsp(self):
        """
            If a bulk sms provider is not defined, the sms can still be sent
            as long as there is a default bulk sms provider
        """
        #set default bsmsp
        name = 'twilio'
        bsmp = BulkSMSProvider.query.filter_by(name=name).first()
        bsmp.default = True
        db.session.commit()

        sdata = {'To': '+254720905558', 'From': '+19386669155',
                'Body': 'Hello, Tests are being run on Microservice SMS App'}

        send_sms_url = self.get_server_url()+'/send-sms/'

        post_resp = requests.post(url=send_sms_url, data=json.dumps(sdata))
        self.assertDictContainsSubset({'bulk_sms_provider': 'twilio'}, post_resp.json())

    #test sending sms with a valid bulk sms provider
    def test_5_send_sms_valid_bsmsp(self):
        sdata = {'To': '+254720905558', 'From': '+19386669155',
                'Body': 'Hello, Tests are being run on Microservice SMS App'}

        send_sms_url = self.get_server_url()+'/send-sms/?service=twilio'

        post_resp = requests.post(url=send_sms_url, data=json.dumps(sdata))
        self.assertDictContainsSubset({'bulk_sms_provider': 'twilio'}, post_resp.json())
    
    #test sending sms with a valid bulk sms provider
    def test_6_send_sms_with_no_data(self):
        send_sms_url = self.get_server_url()+'/send-sms/?service=twilio'

        post_resp = requests.post(url=send_sms_url)
        print(post_resp.json())
        self.assertEqual(post_resp.json(), {'error':'No data was passed'})

    #destory database last
    def test_7_destroy_database(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
