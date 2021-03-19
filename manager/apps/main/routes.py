from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('apps/main/after_signup/dashboard.html')
    return render_template('apps/main/before_signup/home.html') 

