from flask import Blueprint, redirect, request, flash, url_for, render_template, jsonify
from flask_login import login_required, login_user, current_user, logout_user

from manager.apps.inventory.forms import NewConsumableForm

from manager.models import Consumable, Service, Transection
from manager.models import Customer
from manager.ext import db,dbt
from . import inventory

# All Consumable Showcase
@inventory.route('/consumables', methods=['GET','POST'])
def consumables():
    form = NewConsumableForm()
    consumables = dbt.session.query(Consumable).all()
    return render_template('apps/inventory/consumables/all_consumables.html', consumables=consumables, form=form)

# Consumable Info
@inventory.route('/consumables/create', methods=['GET','POST'])
def consumable_create():
    form = NewConsumableForm()
    # Create New Consumable
    if form.validate_on_submit():
        createConsumable(form, dbt)
        return redirect(url_for('inventory.consumables'))
    return redirect(url_for('inventory.consumables'))

# Consumable Info
@inventory.route('/consumable/<c_id>', methods=['GET','POST'])
def consumable_info(c_id):
    consumable = dbt.session.query(Consumable).get_or_404(c_id)
    return render_template('apps/inventory/consumables/consumable_info.html', consumable=consumable)

# Consumable Edit
@inventory.route('/consumables/<c_id>/edit', methods=['GET','POST'])
def consumable_edit(c_id):
    consumable = dbt.session.query(Consumable).get_or_404(c_id)
    return render_template('apps/inventory/consumables/consumable_edit.html', consumable=consumable)

# Consumable Delete
@inventory.route('/consumables/<c_id>/delete', methods=['GET','POST'])
def consumable_delete(c_id):
    consumable = dbt.session.query.get_or_404(c_id)
    if consumable:
        try:
            dbt.session.delete(consumable)
            dbt.session.commit()
        except:
            dbt.session.rollback()
    return redirect(url_for('main.home'))


def createConsumable(form, db):
    consumable = Consumable(    name = form.name.data,
                                product_code = form.product_code.data,
                                category = form.category.data,
                                description = form.description.data,
                                model = form.model.data,
                                unit = form.unit.data,
                                qty = form.qty.data,
                                low_stock_alert = form.low_stock_alert.data,
                                sales_price = form.sales_price.data
                            )
    try:
        dbt.session.add(consumable)
        dbt.session.commit()
    except Exception as e:
        print(e)
        dbt.session.rollback()