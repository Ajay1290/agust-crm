from ..routes import users


from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user

from manager.ext import db, dbt
from manager.apps.users.forms import UpdateCredentials
from manager.models.users import User
from manager.models.func import set_db_for_binders


@users.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    set_db_for_binders(dbt.engine)
    return render_template('apps/main/after_signup/welcome.html')


@users.route('/settings')
@login_required
def settings():
    return render_template('apps/users/settings.html')


@users.route('/settings/update_credentials', methods=['GET', 'POST'])
@login_required
def update_credentials():
    form = UpdateCredentials(current_user, uid=current_user.id)

    if form.validate_on_submit():
        new_password = request.form.get('password', '')
        current_user.email = request.form.get('email')

        if new_password:
            current_user.password = User.encrypt_password(new_password)

        current_user.save()

        flash('Your sign in settings have been updated.', 'success')
        return redirect(url_for('users.settings'))

    return render_template('apps/users/before_signup/update_credentials.html', form=form)
