from datetime import datetime
import enum
from app import db


class BulkSMSProvider(db.Model):

    __tablename__ = 'bulk_sms_providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=True)
    api_endpoint = db.Column(db.String(255), nullable=True)
    headers = db.Column(db.Text, nullable=True)
    username = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)
    default = db.Column(db.Boolean, default=False)

    def __init__(self, name=None, api_endpoint=None, headers=None, username=None, password=None, default=False):
        self.name = name
        self.api_endpoint = api_endpoint
        self.headers = headers
        self.username = username
        self.password = password
        self.default = default

    def __repr__(self):
        return self.name


class DeliveryStatus(enum.Enum):
    SUCCESS = 'success'
    FAIL = 'fail'

class DeliveryReport(db.Model):

    __tablename__ = 'delivery_reports'

    id = db.Column(db.Integer, primary_key=True)
    sms_provider_id = db.Column(db.Integer, db.ForeignKey('bulk_sms_providers.id'))
    date = db.Column(db.DateTime, default=datetime.now())
    sender = db.Column(db.String(20))
    recepient = db.Column(db.String(20))
    response = db.Column(db.JSON())
    status_code = db.Column(db.Integer())

    def __init__(self, sms_provider_id=None, date=None, sender=None, recepient=None, message=None, response=None, status_code=None):
        self.sms_provider_id = sms_provider_id
        self.date = date
        self.sender = sender
        self.recepient = recepient
        self.response = response
        self.status_code = status_code

    def __repr__(self):
        return 'id: {0}, Recepient: {1}, JSON Response: {2}'.format(self.id, self.recepient, self.response)
