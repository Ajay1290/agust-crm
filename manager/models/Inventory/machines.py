from manager.ext import db, dbt
from manager.libs.utils.util_sqlalchemy import ResourceMixin
from .transections import Transection

class Machine(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Info
    name = db.Column(db.String, unique=True, server_default='')
    description = db.Column(db.String, server_default='')
    product_code = db.Column(db.String, server_default='')
    category = db.Column(db.String, server_default='')

    model = db.Column(db.String, server_default='')
    serial = db.Column(db.String,server_default='')
    instdate = db.Column(db.Date, server_default='')

    Customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __init__(self, **kwargs):
        super(Machine, self).__init__(**kwargs)
        self._create_transection('Purchased')

    def _create_transection(self, action):
        transection = Transection(
                        name = f'{self.name} ({self.model} | {self.model})',
                        category = "Machine",
                        action = action,
                        unit = 'UNIT',
                        qty = '1')
        try:
            dbt.session.add(transection)
            dbt.session.commit()
        except Exception as e:
            print(e)
            dbt.session.rollback()