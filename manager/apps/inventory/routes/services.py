from flask import Blueprint, redirect, request, flash, url_for, render_template, jsonify
from flask_login import login_required, login_user, current_user, logout_user

from manager.models import Machine, Service
from manager.models import Customer
from manager.libs.utils.safe_next_url import safe_next_url
from manager.ext import db,dbt
from . import inventory

# All Services
@inventory.route('/services')
def services():
    customers = dbt.session.query(Customer)
    return render_template('apps/inventory/services/all_services.html', customers=customers)