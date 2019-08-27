from flask_admin.contrib.sqla import ModelView
from .models import BulkSMSProvider, DeliveryReport
from app import admin, db

class SMSModelView(ModelView):
    column_labels = {
        'api_endpoint': 'API Endpoint'
    }

class ReportModelView(ModelView):
    can_create = False

admin.add_view(SMSModelView(BulkSMSProvider, db.session, 'Bulk SMS Provider'))
admin.add_view(ReportModelView(DeliveryReport, db.session, 'SMS Delivery Report'))