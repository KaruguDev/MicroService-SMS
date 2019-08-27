import requests
import json


def nexmo_send():
    """
        curl - X POST  https: // rest.nexmo.com/sms/json 
        - d api_key = 750d0256 - d api_secret = OrZgdYLLzs4WzZ5B 
        - d to = 254720905558 - d from = "nexmo" - d text = "Hello from Nexmo"
    """

    url = "https://rest.nexmo.com/sms/json"
    headers = {'Accept':'application/json'}
    data = {'api_key': '750d0256', 'api_secret': 'OrZgdYLLzs4WzZ5B', 'to':'254720905558', 'text': 'Hello from Microservice SMS', 'from':'NEXMO'}
    json_data = json.dumps(data)

    response = requests.post(url=url, data=data)

    return response

#response = nexmo_send()

#print(response.status_code)
#print(response.json())


def at_send():

    url = 'https://api.africastalking.com/version1/messaging'
    test_url = 'https://api.sandbox.africastalking.com/version1/messaging'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'ApiKey':'a7f94b43d1054707ac9f28b0da40602146e99c43a4fadddce86716c9175fc20c',
        'Accept':'application/json'
        }
    test_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'ApiKey': '8e3d658eceebbfd7b9648b9df54b34340c4774602422337b1c400bfe313fdb40',
        'Accept': 'application/json'
    }
    data = {'username':'micro_sms', 'to': '254720905558', 'message': 'Hello from Microservice SMS', 'bulkSMSMode':1}
    json_data = json.dumps(data)

    response = requests.post(url=url, headers=headers, data=data)

    return response

resp = at_send()

print(resp.status_code)
print(resp.headers)
#print(resp.text)
print(resp.json())
