from manager.ext import db 
from manager.libs.utils.util_sqlalchemy import ResourceMixin

class Service(ResourceMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True, server_default='')    
    product_code = db.Column(db.String, server_default='')
    category = db.Column(db.String, server_default='')
    description = db.Column(db.String, server_default='')            
    
    sales_price = db.Column(db.DECIMAL(precision=20, scale=2), server_default='0')
    purchase_price = db.Column(db.DECIMAL(precision=20, scale=2), server_default='0')
    profit = db.Column(db.DECIMAL(precision=20, scale=2), server_default='0')
        
    basis = db.Column(db.String, server_default='')
    cycles = db.Column(db.Integer, server_default='0')
