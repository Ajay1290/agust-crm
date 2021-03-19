from flask import Blueprint, redirect, request, flash, url_for, render_template, jsonify
from flask_login import login_required, login_user, current_user, logout_user

from manager.ext import db, dbt
from manager.models import Complaint, Customer, Machine, Employee
from .forms import NewComplaintForm


calls = Blueprint('calls', __name__, url_prefix='/calls')


# All Complaint
@calls.route('/complaints', methods=["GET","POST"])
def complaints():
    form = NewComplaintForm()
    customers = [(customer.id, customer.display_name)  for customer in dbt.session.query(Customer).all()]
    machines = [(machine.id, machine.name)  for machine in dbt.session.query(Machine).all()]
    employees = [(employee.id, employee.name) for employee in dbt.session.query(Employee).all()]
    complaints = dbt.session.query(Complaint).all()
    return render_template('apps/calls/all_complaints.html', form=form, complaints=complaints,
                                   customers=customers, machines=machines, employees=employees)


# Complaint Info
@calls.route('/complaints/<c_id>', methods=["GET","POST"])
def complaint(c_id):
    return render_template('apps/calls/complaint.html')


# Edit Complaint
@calls.route('/complaints/<c_id>/edit', methods=["GET","POST"])
def edit_complaint(c_id):
    return redirect(url_for('calls.complaints'))


# Create New Complaint
@calls.route('/complaints/create', methods=["GET","POST"])
def create_complaint():
    form = NewComplaintForm()
    if _create_complaint(form, dbt):
        flash("Your Complaints has been registered!",'success')
        return redirect(url_for('calls.complaints'))
    flash("[X] Something went wrong, please Try again!",'danger')
    return redirect(url_for('calls.complaints'))


def _create_complaint(form, db):
    complaint = Complaint(
        nature = form.nature.data,
        description = form.description.data,
        contact_name = form.contact_name.data,
        contact_phone = form.contact_phone.data,
        source = form.source.data,
        Machine_id = form.machine.data,
        Machine_Customer_id = dbt.session.query(Customer).filter(
                                form.machine.id in [machine.id  for machine in Customer.machines]
                                ),
        Employee_id = form.employee.data
    )
    try:
        db.session.add(complaint)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
