from manager.ext import db, dbt
from manager.libs.utils.util_sqlalchemy import ResourceMixin
from .transections import Transection

class Consumable(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Info
    name = db.Column(db.String, unique=True, server_default='')
    description = db.Column(db.String, server_default='')
    model = db.Column(db.String, server_default='')
    product_code = db.Column(db.String, server_default='')
    category = db.Column(db.String, server_default='')
    hsn = db.Column(db.String, server_default='')
    
    # Inventory
    unit = db.Column(db.String, server_default='')
    qty = db.Column(db.Integer, server_default='0')
    low_stock_alert = db.Column(db.Integer, server_default='0')

    # Sales
    sales_price = db.Column(db.DECIMAL(precision=20, scale=2), server_default='0')

    def __init__(self, **kwargs):
        super(Consumable, self).__init__(**kwargs)
        self._create_transection('Purchased', self.qty)

    def _create_transection(self, action, qty):
        transection = Transection(
                        name = f'{self.name} ({self.model})',
                        category = "Consumable",
                        action = action,
                        unit = self.unit,
                        qty = qty)
        try:
            dbt.session.add(transection)
            dbt.session.commit()
        except Exception as e:
            print(e)
            dbt.session.rollback()


# -----Relations-------------------------------------------------------

complaint_has_cosnumable = db.Table('complaint_has_cosnumable',
    db.Column('Complaint_id', db.Integer, db.ForeignKey('complaint.id')),
    db.Column('Complaint_Machine_id', db.Integer, db.ForeignKey('machine.id')),
    db.Column('Complaint_Machine_Customer_id', db.Integer, db.ForeignKey('customer.id')),
    db.Column('Consumable_id', db.Integer, db.ForeignKey('consumable.id')),
)