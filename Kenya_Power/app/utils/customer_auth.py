"""
Customer Portal Authentication Utilities
Session-based authentication for customer portal (separate from staff auth)
"""
from functools import wraps
from flask import session, redirect, url_for, flash, g
from datetime import datetime


def login_customer(customer):
    """
    Log in a customer by storing their ID in session

    Args:
        customer: Customer model instance
    """
    session['customer_id'] = customer.customer_id
    session['customer_logged_in'] = True
    customer.last_login = datetime.utcnow()


def logout_customer():
    """Log out the current customer by clearing session data"""
    session.pop('customer_id', None)
    session.pop('customer_logged_in', None)


def get_current_customer():
    """
    Get the currently logged in customer from session

    Returns:
        Customer instance or None
    """
    from app.models import Customer

    if session.get('customer_logged_in') and session.get('customer_id'):
        return Customer.query.get(session['customer_id'])
    return None


def customer_login_required(f):
    """
    Decorator to require customer login for a route

    Usage:
        @customer_bp.route('/dashboard')
        @customer_login_required
        def dashboard():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        customer = get_current_customer()
        if not customer:
            flash('Please log in to access the customer portal.', 'info')
            return redirect(url_for('customer.login'))

        # Make customer available in g for the request
        g.customer = customer
        return f(*args, **kwargs)
    return decorated_function
