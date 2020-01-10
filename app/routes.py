from flask import render_template, send_from_directory, url_for, request, jsonify
from ast import literal_eval
import json
from app import app, db
from .models import BulkSMSProvider, DeliveryReport
from .send_sms import SendSMS


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/send-sms/', methods=['POST'])
def send_sms():
    service_provider = request.args.get('service')

    #get the specified bulk sms provider
    bulk_sms_provider = BulkSMSProvider.query.filter_by(name=service_provider).first()

    #select the default bulk sms provider if the specified one was not found
    if not bulk_sms_provider:
        bulk_sms_provider = BulkSMSProvider.query.filter_by(default=True).first()

    #return error if the specified and default bulk sms provider were not found
    if not bulk_sms_provider:
        if service_provider:
            return jsonify({'error': f'{service_provider} is not supported yet'}), 400

        else:
            return jsonify({'error': 'Bulk SMS Provider has not been defined'}), 400
        
            
    #Instantiate send SMS
    send_sms = SendSMS(bulk_sms_provider)

    if not request.data:
        return jsonify({'error': 'No data was passed'}), 400

    #convert bytes back to dict
    if type(request.data) == bytes:
        #convert bytes data type to dictionary
        data = json.loads(request.data.decode('utf-8').replace("'", '"'))
        
    #convert string into dict
    elif type(request.data) == str:
        #convert str data type to dictionary
        data = literal_eval(request.data)

    else:
        data = request.data

    if 'to' not in data:
        return jsonify({'error': 'No sender'}), 400

    else:
        msg_data = {}

        if bulk_sms_provider.name == 'nexmo':
            msg_data.update(data)
            extra_data = {'api_key':app.config['NEXMO_API_KEY'], 'api_secret':app.config['NEXMO_API_SECRET'],\
                            'text':data['message'], 'from':'nexmo'}
            msg_data.update(extra_data)
    
        elif bulk_sms_provider.name == 'twilio':
            twilio_data = {'To':f'+{data["to"]}', 'Body':data['message'], 'From':app.config['TWILIO_FROM']}
            msg_data.update(twilio_data)
            
        elif bulk_sms_provider.name == 'africas_talking':
            msg_data.update(data)
            extra_data = {'username':app.config['AFRICAS_TALKING_USERNAME'], 'bulkSMSMode':1}
            msg_data.update(extra_data)

        else:
            pass
   
    send_sms.sms_queue(msg_data)
    response = send_sms.send()

    if response.headers.get('content-type') == 'application/json':
        response_from_provider = response.json()
    else:
        response_from_provider = response.text

    #create delivery report
    data_lower = {k.lower():v for k,v in msg_data.items()}
    recepient = data_lower['to']
    dreport = DeliveryReport(
                sms_provider_id=bulk_sms_provider.id, sender=bulk_sms_provider.name, 
                recepient=recepient, response=response_from_provider, status_code=response.status_code
            )
    db.session.add(dreport)
    db.session.commit()

    #return response
    return jsonify({'bulk_sms_provider':bulk_sms_provider.name, 'response_from_provider': response_from_provider}), response.status_code


# 404 ROUTE
@app.errorhandler(404)
def error_404(e):
    return render_template('404.html', title='404'), 404
