from ..routes import users
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request, session
from flask_login import login_required, login_user, logout_user, current_user

from manager.ext import db, dbt

from manager.models import User

from manager.libs.mail import send_email
from manager.libs.decorators import anonymous_required
from manager.libs.utils.safe_next_url import safe_next_url

from manager.apps.users.forms import SignupForm, LoginForm, UpdateCredentials, SendEmailAgainForm
from manager.apps.users.forms import BeginPasswordResetForm, PasswordResetForm

# Sign Up PAGE
@users.route('/signup', methods=['GET', 'POST'])
@anonymous_required()
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data.lower(), 
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()

            if login_user(user):
                dbt.create_db_for_tenant(app=current_app, tenant_name=user.username)
                dbt.choose_tenant(user.username)
                flash('Awesome, thanks for signing up!', 'success')
                return redirect(url_for('users.welcome'))
        except Exception as e:
            print(e)
            db.session.rollback()
            flash(f'Not Worked! {e}', 'danger')
            return redirect(url_for('users.signup'))
        # # Email Confirmation Process Started.
        # token = User.confirm_email_token(form.username.data.lower(), form.email.data.lower(), form.password.data)
        # confirm_url = url_for('users.email_confirmed', token=token, _external=True)
        # html = render_template('apps/users/mails/confirm_email.html',username=form.username.data.lower(), confirm_url=confirm_url)
        # try:
        #     send_email(to=form.email.data.lower(), subject='Email Confirmation - [ Agust CRM ]', template=html)
        # except Exception as e:
        #     print(e)
        #     flash('Something went Wrong!', 'danger')
        #     return redirect(url_for('users.signup'))
        # # ###----------------------------
        
        # flash('You need to confirm your email to start your journey with us.', 'secondary')
        # return redirect(url_for('users.confirm_email', token=token))
    
    return render_template('apps/users/auth/signup.html', form=form)


# Confirm Email PAGE
@users.route('/confirm-email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    data = User.deserialize_token(token)
    form = SendEmailAgainForm()
    if form.validate_on_submit():
        confirm_url = url_for('users.email_confirmed', token=token, _external=True)
        html = render_template('apps/users/mails/confirm_email.html', username=data['user_username'], confirm_url=confirm_url)
        send_email(to=data['user_email'], subject='Email Confirmation - [ Agust CRM ]', template=html)

        flash('We have send you email again check this time it may took longer than usual sometime.', 'secondary')
        return redirect(url_for('users.confirm_email', token=token))

    return render_template('apps/users/auth/confirm_email/confirm_email.html', form=form, data=data)


# Email Confirmed PAGE
@users.route('/email-confirmed/<token>', methods=['GET', 'POST'])
def email_confirmed(token):
    try:
        data = User.deserialize_token(token)
    except:
        flash('The confirmation link is invalid or has expired, please ask for send again email.', 'danger')
        return redirect(url_for('users.confirm_email'))
    user = User.find_by_identity(data['user_username'])
    if user:
        flash('Account already confirmed.', 'success')
        login_user(user)
        return redirect(url_for('main.home'))
    else:
        # New User will be added to database.
        user = User(username=data['user_username'], email=data['user_email'], password=data['user_password'])
        try:
            db.session.add(user)
            user.email_confirmed = True
            db.session.commit()
            addNewDatabase(user)
            # Email Sent For Welcome.
            html = render_template('apps/users/mails/welcome.html', user=user)
            send_email(to=data['user_email'], subject='Welcome - [ Agust CRM ]', template=html)
            # ###----------------------------
        except Exception as e:
            print(e)
            db.session.rollback()
        # ###----------------------------
        login_user(user)

        flash('You have confirmed your account. Thank you, for your coopreation.', 'success')
        return redirect(url_for('billing.pricing'))
    
    return redirect(url_for('main.home'))


def addNewDatabase(user):
    print(dbt.engine)
    dbt.create_db_for_tenant(app=current_app, tenant_name=user.username)
    User.__table__.create(bind=dbt.engine, checkfirst=True)
    user_dbt = User(username=user.username, password=user.password, email=user.email, phone=user.phone)
    dbt.session.add(user_dbt)
    dbt.session.commit()


# Login PAGE
@users.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))
    if form.validate_on_submit():
        u = User.find_by_identity(form.identity.data)
        if u and u.authenticated(password=form.password.data):
            is_remembered = request.form.get('remember', False)
            if login_user(u, remember=is_remembered) and u.is_active():
                dbt.choose_tenant(u.username)
                # u.update_activity_tracking(request.remote_addr)
                # if u.subscription:
                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))
                return redirect(url_for('main.home'))
            else:
                flash('This account has been disabled.', 'danger')
        else:
            flash('Identity or password is incorrect.', 'danger')
    return render_template('apps/users/auth/login.html', form=form)


# LOGOUT PAGE
@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('users.login'))



@users.route('/account/begin_password_reset', methods=['GET', 'POST'])
@anonymous_required()
def begin_password_reset():
    form = BeginPasswordResetForm()

    if form.validate_on_submit():
        u = User.initialize_password_reset(request.form.get('identity'))

        flash('An email has been sent to {0}.'.format(u.email), 'success')
        return redirect(url_for('users.login'))

    return render_template('apps/main/before_signup/auth/begin_password_reset.html', form=form)


@users.route('/account/password_reset', methods=['GET', 'POST'])
@anonymous_required()
def password_reset():
    form = PasswordResetForm(reset_token=request.args.get('reset_token'))

    if form.validate_on_submit():
        u = User.deserialize_token(request.form.get('reset_token'))

        if u is None:
            flash('Your reset token has expired or was tampered with.',
                  'danger')
            return redirect(url_for('users.begin_password_reset'))

        form.populate_obj(u)
        u.password = User.encrypt_password(request.form.get('password'))
        u.save()

        if login_user(u):
            flash('Your password has been reset.', 'success')
            return redirect(url_for('users.settings'))

    return render_template('apps/main/before_signup/auth/password_reset.html', form=form)