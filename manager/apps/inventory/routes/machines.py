from flask import Blueprint, redirect, request, flash, url_for, render_template, jsonify
from flask_login import login_required, login_user, current_user, logout_user

from manager.apps.inventory.forms import NewMachineForm, AssignCustomerForm

from manager.models import Machine, Service
from manager.models import Customer
from manager.ext import db,dbt
from . import inventory


# All Machine Showcase
@inventory.route('/machines', methods=['GET','POST'])
def machines():
    form = NewMachineForm()
    a_form = AssignCustomerForm()
    machines = dbt.session.query(Machine).all()
    customers = dbt.session.query(Customer).all()
    return render_template('apps/inventory/machines/all_machines.html', machines=machines, 
                                                customers=customers,form=form, a_form=a_form)


# Machine Info
@inventory.route('/machines/create', methods=['GET','POST'])
def machine_create():
    form = NewMachineForm()
    if form.validate_on_submit():
        createMachine(form, dbt) # Create New Machine
        return redirect(url_for('inventory.machines'))
    return redirect(url_for('inventory.machines'))


# Machine Info
@inventory.route('/machine/<m_id>', methods=['GET','POST'])
def machine_info(m_id):
    machine = dbt.session.query(Machine).get_or_404(m_id)
    return render_template('apps/inventory/machines/machine_info.html', machine=machine)


# Machine Edit
@inventory.route('/machines/<m_id>/edit', methods=['GET','POST'])
def machine_edit(m_id):
    machine = dbt.session.query(Machine).get_or_404(m_id)
    return render_template('apps/inventory/machines/machine_edit.html', machine=machine)


# Machine Delete
@inventory.route('/machines/<m_id>/delete', methods=['GET','POST'])
def machine_delete(m_id):
    machine = dbt.session.query.get_or_404(m_id)
    if machine:
        try:
            dbt.session.delete(machine)
            dbt.session.commit()
        except:
            dbt.session.rollback()
    return redirect(url_for('main.home'))


# Machine Assign
@inventory.route('/machines/<m_id>/assign', methods=['GET','POST'])
def assign_machine(m_id):
    machine = dbt.session.query(Machine).get_or_404(m_id)
    try:
        if not request.form.get('customer_id') == '-1':
            machine.Customer_id = request.form.get('customer_id')
            dbt.session.commit()
            flash("Customer has been assigned to Machine", 'success')
            return redirect(url_for('inventory.machines'))
        else:
            raise ValueError
    except Exception as e:
        print(e)
        dbt.session.rollback()
        flash("[x] Something Went Wrong Please Try Again!", 'danget')
        return redirect(url_for('inventory.machines'))


def createMachine(form, db):
    machine = Machine(  name = form.name.data,
                        product_code = form.product_code.data,
                        category = form.category.data,
                        description = form.description.data,
                        model = form.model.data,
                        serial = form.serial.data,
                        instdate = form.instdate.data)
    try:
        dbt.session.add(machine)
        dbt.session.commit()
    except Exception as e:
        print(e)
        dbt.session.rollback()