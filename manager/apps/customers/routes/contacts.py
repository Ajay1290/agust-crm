from flask import redirect, request, flash, url_for, render_template, jsonify

from ..forms import NewContactForm, EditContactForm
from manager.models import Customer, Contact
from manager.ext import dbt

from ..routes import customers
from .helpers import create_new_contact

@customers.route('/contacts', methods=['GET','POST'])
def all_contacts():        
    c_form = NewContactForm()
    contacts =  dbt.session.query(Contact).all()
    customers =  dbt.session.query(Customer).all()
    print(customers)
    if request.get_json():
        response = request.get_json()
        contacts =  dbt.session.query(Contact).filter(Contact.is_active == True).limit(int(response['customer_len']))
        customer_fields = list(c_form._fields)
        customer_dict = {}
        for i in range(len(contacts)):
            customer_data = {}
            for field in customer_fields:
                customer_data[field] = contacts[i].__getattribute__(field)
            customer_dict[i] = customer_data
        return jsonify(customer_dict)
    if c_form.validate_on_submit():
        create_new_contact(c_form, dbt)
        return redirect(url_for('customers.all_contacts'))
    return render_template('apps/customers/contacts/all_contacts.html',c_form=c_form, contacts=contacts, customers=customers)