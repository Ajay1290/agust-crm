from .users import User, Company
from .Customer import Contact, Customer, customer_has_contact
from .Complaint import Complaint, Employee
from .Inventory import Machine, Service, Consumable, complaint_has_cosnumable, Transection

def set_db_for_binders(engine):
    User.__table__.create(bind=engine, checkfirst=True)
    Company.__table__.create(bind=engine, checkfirst=True)
    Customer.__table__.create(bind=engine, checkfirst=True)
    Contact.__table__.create(bind=engine, checkfirst=True)
    Complaint.__table__.create(bind=engine, checkfirst=True)
    Employee.__table__.create(bind=engine, checkfirst=True)
    Machine.__table__.create(bind=engine, checkfirst=True)
    Transection.__table__.create(bind=engine, checkfirst=True)
    Consumable.__table__.create(bind=engine, checkfirst=True)
    Service.__table__.create(bind=engine, checkfirst=True)

    complaint_has_cosnumable.create(bind=engine, checkfirst=True)
    customer_has_contact.create(bind=engine, checkfirst=True)

