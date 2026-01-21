"""
Custom decorators for role-based access control
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def role_required(*roles):
    """
    Decorator to restrict access based on user roles

    Usage:
        @role_required('admin', 'manager')
        def admin_only_view():
            pass
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))

            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.dashboard'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator