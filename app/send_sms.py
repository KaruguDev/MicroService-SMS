from ast import literal_eval
from pythonds import Queue
import requests
import json

class SendSMS:

    def __init__(self, bulk_sms_provider):
        self.bulk_sms_provider = bulk_sms_provider
        self.msg_queue = Queue()

    def sms_queue(self, data):
        self.msg_queue.enqueue({'data':data})

    def send(self):
        while not self.msg_queue.isEmpty():
            msg = self.msg_queue.dequeue()
            bulk_sms_provider = self.bulk_sms_provider

            url = bulk_sms_provider.api_endpoint
            headers = literal_eval(bulk_sms_provider.headers) #convert str to dict datatype
            data = msg['data']
            
            if bulk_sms_provider.username and bulk_sms_provider.password:
                response = requests.post(url=url, headers=headers, data=data, auth=(bulk_sms_provider.username, bulk_sms_provider.password))
            else:
                response = requests.post(url=url, headers=headers, data=data)
            
            return response

