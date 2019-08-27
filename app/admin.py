from flask_admin.contrib.sqla import ModelView
from .models import BulkSMSProvider, DeliveryReport
from app import admin, db

class AppModelView(ModelView):
    column_labels = {
        'api_endpoint': 'API Endpoint'
    }

admin.add_view(AppModelView(BulkSMSProvider, db.session, 'Bulk SMS Provider'))
admin.add_view(AppModelView(DeliveryReport, db.session, 'SMS Delivery Report'))