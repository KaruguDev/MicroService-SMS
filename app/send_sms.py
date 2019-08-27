from pythonds import Queue
import requests

class SendSMS:

    def __init__(self, bulk_sms_provider):
        self.bulk_sms_provider = bulk_sms_provider
        self.msg_queue = Queue()

    def msg_queue(self, data):
        #Queue Messages
        self.msg_queue.enqueue({'bulk_sms_provider':self.bulk_sms_provider, 'data':data, 'counter':0})

    def send(self):
        if not self.msg_queue.isEmpty():
            #send message

            #if response sucessful

            #else queue back the message and increment the counter