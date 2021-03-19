from functools import wraps

import stripe

from flask import redirect, url_for, flash
from flask_login import current_user


def anonymous_required(url='/'):
    """
    Redirect a user to a specified location if they are already signed in.

    :param url: URL to be redirected to if invalid
    :type url: str
    :return: Function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                flash('You are already authenticated.', "info")
                return redirect(url)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def role_required(*roles):
    """
    Does a user have permission to view this page?

    :param *roles: 1 or more allowed roles
    :return: Function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash('You do not have permission to do that.', 'danger')
                return redirect('/')

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def subscription_required(f):
    """Ensure a user is subscribed, if not redirect them to the pricing table.

    :return: Function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.subscription:
            return redirect(url_for('billing.pricing'))

        return f(*args, **kwargs)

    return decorated_function


def handle_stripe_exceptions(f):
    """Handle Stripe exceptions so they do not throw 500s.

    :param f:
    :type f: Function
    :return: Function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except stripe.error.CardError:
            flash('Sorry, your card was declined. Try again perhaps?', 'danger')
            return redirect(url_for('user.settings'))
        except stripe.error.InvalidRequestError as e:
            flash(e, 'danger')
            return redirect(url_for('user.settings'))
        except stripe.error.AuthenticationError:
            flash('Authentication with our payment gateway failed.', 'danger')
            return redirect(url_for('user.settings'))
        except stripe.error.APIConnectionError:
            flash(
                'Our payment gateway is experiencing connectivity issues'
                ', please try again.', 'danger')
            return redirect(url_for('user.settings'))
        except stripe.error.StripeError:
            flash(
                'Our payment gateway is having issues, please try again.',
                'danger')
            return redirect(url_for('user.settings'))

    return decorated_function
