from datetime import datetime
import enum
from app import db


class BulkSMSProvider(db.Model):

    __tablename__ = 'bulk_sms_providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=True)
    api_endpoint = db.Column(db.String(255), nullable=True)
    headers = db.Column(db.JSON, nullable=True)
    status_codes = db.Column(db.String(100))

    def __init__(self, name=None, send_sms_url=None, headers=None, status_codes=None):
        self.name = name
        self.api_endpoint = api_endpoint
        self.headers = headers
        self.status_codes = status_codes

    def __repr__(self):
        return self.name


class Status(enum.Enum):
    success = 'Success'
    fail = 'Fail'

class DeliveryReport(db.Model):

    __tablename__ = 'delivery_reports'

    id = db.Column(db.Integer, primary_key=True)
    sms_provider_id = db.Column(db.Integer, db.ForeignKey('bulk_sms_providers.id'))
    sender = db.Column(db.String(20))
    message = db.Column(db.String(255))
    recepient = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Enum(Status))

    def __init__(self, sms_provider_id=None, sender=None, message=None, recepient=None):
        self.sms_provider_id = sms_provider_id
        self.sender = sender
        self.message = message
        self.recepient = recepient

    def __repr__(self):
        return 'id: {0}, Recepient: {1}, Message: {2}'.format(self.id, self.recepient, self.message)
