from manager import create_app, db, dbt
from faker import Faker
from manager.models import Customers

app = create_app()

fake = Faker()
app.config.update(SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:apku1290@localhost:5432/qqq')
with app.app_context():
    for _ in Customers.query.filter(Customers.id > 1).limit(1000):
        db.session.delete(_)
        db.session.commit()
    # for _ in range(1000):
    #     customer = Customers()
    #     customer.first_name = fake.first_name()
    #     customer.last_name = fake.last_name()
    #     customer.company = fake.company()
    #     customer.display_name = f'{fake.prefix_male()} {customer.first_name} {customer.last_name}'
    #     # Contant Info
    #     customer.phone = fake.phone_number()[:13]
    #     customer.email = fake.email()
    #     # Billing Address
    #     customer.address = fake.address()
    #     customer.city = fake.city()
    #     customer.state = fake.state()
    #     customer.country = fake.country()

    #     # Shiping Address
    #     customer.s_address = fake.address()
    #     customer.s_city = fake.city()
    #     customer.s_state = fake.state()
    #     customer.s_country = fake.country()
        
    #     db.session.add(customer)
    #     db.session.commit()