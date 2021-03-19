import pytz
from datetime import datetime
from collections import OrderedDict
from manager.ext import db
from manager.libs.utils.util_sqlalchemy import AwareDateTime

class Transection(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Info
    name = db.Column(db.String, unique=True, server_default='')
    category = db.Column(db.String, server_default='')
    action = db.Column(db.String, server_default='')

    # Inventory
    unit = db.Column(db.String, server_default='')
    qty = db.Column(db.Integer, server_default='0')

    remark = db.Column(db.Text(200), server_default='')

    created_on = db.Column(AwareDateTime())
