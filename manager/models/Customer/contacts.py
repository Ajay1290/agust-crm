from manager.ext import db,dbt
from manager.libs.utils.util_sqlalchemy import ResourceMixin

class Contact(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)

    # Contact Info
    phone = db.Column(db.String(15), server_default='')
    email = db.Column(db.String(45), server_default='')    
    website = db.Column(db.String(255), server_default='')

    Customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

# -----Relations-------------------------------------------------------

customer_has_contact = db.Table('customer_has_contact',
    db.Column('Customer_id', db.Integer, db.ForeignKey('customer.id')),
    db.Column('Contact_id', db.Integer, db.ForeignKey('contact.id')),
)