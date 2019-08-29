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

    #Get Bulk SMS Provider Object
    bulk_sms_provider = BulkSMSProvider.query.filter_by(name=service_provider).first()

    if not bulk_sms_provider:
        #select default bulk sms provider
        bulk_sms_provider = BulkSMSProvider.query.filter_by(default=True).first()

    if not bulk_sms_provider:
        # Return error since bulk sms provider has not been defined
        return jsonify({'error': 'Bulk SMS Provider has not been defined'}), 400

    #Instantiate send SMS
    send_sms = SendSMS(bulk_sms_provider)

    if not request.data:
        return jsonify({'error': 'No data was passed'}), 400

    if type(request.data) == bytes:
        #convert bytes data type to dictionary
        data = json.loads(request.data.decode('utf-8').replace("'", '"'))

    elif type(request.data) == str:
        #convert str data type to dictionary
        data = literal_eval(request.data)

    else:
        data = request.data

    send_sms.sms_queue(data)
    response = send_sms.send()

    if response.headers.get('content-type') == 'application/json':
        response_from_provider = response.json()
    else:
        response_from_provider = response.text

    #create delivery report
    data_lower = {k.lower():v for k,v in data.items()}
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
