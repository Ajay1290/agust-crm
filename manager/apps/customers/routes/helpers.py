from flask import request
from manager.models import Customer, Contact
from manager.ext import dbt

def create_new_customer(c_form, db):            
    customer = Customer(first_name = c_form.first_name.data,
                        last_name = c_form.last_name.data,
                        display_name = c_form.display_name.data,
                        company = c_form.company.data,
                        customer_type = c_form.customer_type.data,
                        phone = c_form.phone.data,
                        email = c_form.email.data,
                        website = c_form.website.data,
                        address = c_form.address.data,
                        pincode = c_form.pincode.data,
                        city = c_form.city.data,
                        state = c_form.state.data,
                        country = c_form.country.data,
                        s_address = c_form.s_address.data,
                        s_pincode = c_form.s_pincode.data,
                        s_city = c_form.s_city.data,
                        s_state = c_form.s_state.data,
                        s_country = c_form.s_country.data,
                        gst = c_form.gst.data,
                        pan = c_form.pan.data)
    db.session.add(customer)
    db.session.commit()

def edit_customer(c_form, db, customer_id):
    customer = dbt.session.query(Customer).get_or_404(customer_id)
    if c_form.validate_on_submit():
        customer.first_name = c_form.first_name.data
        customer.last_name = c_form.last_name.data
        customer.company = c_form.company.data
        customer.display_name = c_form.display_name.data
        customer.customer_type = c_form.customer_type.data
        customer.email = c_form.email.data            
        customer.phone = c_form.phone.data
        customer.website = c_form.website.data
        customer.address = c_form.address.data            
        customer.pincode = c_form.pincode.data
        customer.city = c_form.city.data            
        customer.state = c_form.state.data
        customer.country  = c_form.country.data
        customer.s_address = c_form.address.data
        customer.s_pincode = c_form.s_pincode.data
        customer.s_city = c_form.s_city.data
        customer.s_state = c_form.s_state.data
        customer.s_country = c_form.s_country.data
        customer.gst = c_form.gst.data
        customer.pan = c_form.pan.data
        db.session.commit()

def create_new_contact(c_form, db):            
    contact = Contact(name=c_form.name.data,
                      email=c_form.email.data,
                      phone=c_form.phone.data,
                      website=c_form.website.data,
                      Customer_id=request.form.get('Customer_id'))
    db.session.add(contact)
    db.session.commit()