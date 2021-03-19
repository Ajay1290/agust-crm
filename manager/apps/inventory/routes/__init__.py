from flask import Blueprint, redirect, request, flash, url_for, render_template, jsonify
from flask_login import login_required, login_user, current_user, logout_user

from manager.models import Transection
from manager.libs.utils.safe_next_url import safe_next_url
from manager.ext import db,dbt

inventory = Blueprint('inventory', __name__, url_prefix='/inventory')


# Inventorial Transections
@inventory.route('/transections')
def transections():
    transections = dbt.session.query(Transection).all()
    ctx = transections_ctx()
    return render_template('apps/inventory/transections/all_transections.html', 
                            transections=transections, ctx=ctx)

def transections_ctx():
    total_purchased = dbt.session.query(Transection).filter(Transection.action == "Purchased").count()
    total_sold = dbt.session.query(Transection).filter(Transection.action == "Sold").count()
    return {'purchased':total_purchased, 'sold':total_sold}

from .machines import *
from .services import *
from .consumables import *