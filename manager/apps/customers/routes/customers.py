from flask import Blueprint, redirect, request, flash, url_for, render_template, jsonify

from ..forms import NewCustomerForm, EditCustomerForm
from manager.models import Customer, Contact
from manager.ext import dbt

from ..routes import customers

from .helpers import create_new_customer, edit_customer

@customers.route('/customers', methods=['GET','POST'])
def all_customers():        
    c_form = NewCustomerForm()    
    customers =  dbt.session.query(Customer).filter(Customer.is_active == True)
    if request.get_json():
        response = request.get_json()
        customers =  dbt.session.query(Customer).filter(Customer.is_active == True).limit(int(response['customer_len']))
        customer_fields = list(c_form._fields)
        customer_dict = {}
        for i in range(len(customers)):
            customer_data = {}
            for field in customer_fields:
                customer_data[field] = customers[i].__getattribute__(field)
            customer_dict[i] = customer_data
        return jsonify(customer_dict)
    if c_form.validate_on_submit():
        create_new_customer(c_form, dbt)
        return redirect(url_for('customers.all_customers'))        
    return render_template('apps/customers/customers/all_customers.html',c_form=c_form, customers=customers)

@customers.route('/customers/<customer_id>', methods=['GET','POST'])
def customer_info(customer_id):
    c_form = EditCustomerForm()
    customer = dbt.session.query(Customer).get_or_404(customer_id)
    if request.method == 'GET':        
        c_form.first_name.data = customer.first_name
        c_form.last_name.data = customer.last_name
        c_form.company.data = customer.company
        c_form.display_name.data = customer.display_name
        c_form.customer_type.data = customer.customer_type
        c_form.email.data = customer.email
        c_form.phone.data = customer.phone
        c_form.website.data = customer.website
        c_form.address.data = customer.address
        c_form.pincode.data = customer.pincode
        c_form.city.data = customer.city
        c_form.state.data = customer.state
        c_form.country.data = customer.country
        c_form.s_address.data = customer.s_address
        c_form.s_pincode.data = customer.s_pincode
        c_form.s_city.data = customer.s_city
        c_form.s_state.data = customer.s_state
        c_form.s_country.data = customer.s_country
        c_form.gst.data = customer.gst
        c_form.pan.data = customer.pan
    if c_form.validate_on_submit():
        edit_customer(c_form,dbt,customer_id)
        return redirect(url_for('customers.customer_info', customer_id=customer_id))
    return render_template('apps/customers/customers/customer_info.html', customer=customer, c_form=c_form)

@customers.route('/customers/<customer_id>/inactive', methods=['GET','POST'])
def customer_inactive(customer_id):    
    customer = dbt.session.query(Customer).get_or_404(customer_id)
    customer.is_active = False
    dbt.session.commit()
    return redirect(url_for('customers.customer_info', customer_id=customer_id))

@customers.route('/customers/<customer_id>/active', methods=['GET','POST'])
def customer_active(customer_id):
    customer = dbt.session.query(Customer).get_or_404(customer_id)
    customer.is_active = True
    dbt.session.commit()
    return redirect(url_for('customers.customer_info', customer_id=customer_id))

@customers.route('/customers/<customer_id>/delete', methods=['GET','POST'])
def customer_delete(customer_id):    
    customer = dbt.session.query(Customer).get_or_404(customer_id)
    dbt.session.delete(customer)
    dbt.session.commit()
    return redirect(url_for('customers.all_customers', customer_id=customer_id))