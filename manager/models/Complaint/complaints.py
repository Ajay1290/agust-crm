from manager.ext import db,dbt
from manager.libs.utils.util_sqlalchemy import ResourceMixin, AwareDateTime

class Complaint(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    nature = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80))
    contact_name = db.Column(db.String(80))
    contact_phone = db.Column(db.String(80))
    source = db.Column(db.String(80))

    completed_on = db.Column(AwareDateTime())


    Machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'))
    Machine_Customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    Employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
