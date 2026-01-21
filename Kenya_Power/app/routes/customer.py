"""
Customer Portal Routes
All routes for the customer-facing portal
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, g
from app.models import Customer, Connection, Fault, FaultUpdate, ServiceRequest, Notification, CustomerMessage, User
from app import db
from app.utils.customer_auth import login_customer, logout_customer, customer_login_required, get_current_customer
from datetime import datetime

customer_bp = Blueprint('customer', __name__)


# ============================================
# Authentication Routes
# ============================================

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Customer login page"""
    # If already logged in, redirect to dashboard
    if get_current_customer():
        return redirect(url_for('customer.dashboard'))

    if request.method == 'POST':
        account_number = request.form.get('account_number')
        password = request.form.get('password')

        customer = Customer.query.filter_by(account_number=account_number).first()

        if customer and customer.portal_registered and customer.check_password(password):
            if not customer.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return render_template('customer/login.html')

            login_customer(customer)
            db.session.commit()
            flash(f'Welcome back, {customer.first_name}!', 'success')
            return redirect(url_for('customer.dashboard'))
        elif customer and not customer.portal_registered:
            flash('You have not registered for the portal yet. Please register first.', 'warning')
            return redirect(url_for('customer.register'))
        else:
            flash('Invalid account number or password.', 'danger')

    return render_template('customer/login.html')


@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Portal registration for existing customers"""
    if get_current_customer():
        return redirect(url_for('customer.dashboard'))

    if request.method == 'POST':
        account_number = request.form.get('account_number')
        id_number = request.form.get('id_number')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Find customer by account number
        customer = Customer.query.filter_by(account_number=account_number).first()

        if not customer:
            flash('No customer found with that account number.', 'danger')
        elif customer.portal_registered:
            flash('This account is already registered. Please log in.', 'warning')
            return redirect(url_for('customer.login'))
        elif customer.id_number != id_number:
            flash('ID number does not match our records.', 'danger')
        elif customer.phone != phone:
            flash('Phone number does not match our records.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
        else:
            # Register the customer
            customer.set_password(password)
            customer.portal_registered = True
            try:
                db.session.commit()
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('customer.login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Registration failed: {str(e)}', 'danger')

    return render_template('customer/register.html')


@customer_bp.route('/logout')
def logout():
    """Customer logout"""
    logout_customer()
    flash('You have been logged out.', 'info')
    return redirect(url_for('customer.login'))


# ============================================
# Dashboard
# ============================================

@customer_bp.route('/dashboard')
@customer_login_required
def dashboard():
    """Customer dashboard with overview stats"""
    customer = g.customer

    # Get stats
    active_connections = customer.connections.filter_by(connection_status='active').count()
    pending_faults = customer.reported_faults.filter(Fault.status.notin_(['resolved', 'closed'])).count()
    pending_requests = customer.service_requests.filter(ServiceRequest.status.notin_(['completed', 'rejected'])).count()
    unread_notifications = Notification.query.filter_by(customer_id=customer.customer_id, is_read=False).count()

    # Recent faults
    recent_faults = customer.reported_faults.order_by(Fault.reported_date.desc()).limit(5).all()

    # Recent requests
    recent_requests = customer.service_requests.order_by(ServiceRequest.submitted_date.desc()).limit(5).all()

    return render_template('customer/dashboard.html',
                           customer=customer,
                           active_connections=active_connections,
                           pending_faults=pending_faults,
                           pending_requests=pending_requests,
                           unread_notifications=unread_notifications,
                           recent_faults=recent_faults,
                           recent_requests=recent_requests)


# ============================================
# Connections
# ============================================

@customer_bp.route('/connections')
@customer_login_required
def my_connections():
    """List customer's connections"""
    customer = g.customer
    connections = customer.connections.order_by(Connection.created_at.desc()).all()
    return render_template('customer/my_connections.html', connections=connections, customer=customer)


@customer_bp.route('/connections/<int:connection_id>')
@customer_login_required
def view_connection(connection_id):
    """View connection details"""
    customer = g.customer
    connection = Connection.query.filter_by(
        connection_id=connection_id,
        customer_id=customer.customer_id
    ).first_or_404()

    # Get recent faults for this connection
    recent_faults = Fault.query.filter_by(connection_id=connection_id).order_by(Fault.reported_date.desc()).limit(5).all()

    return render_template('customer/view_connection.html',
                           connection=connection,
                           customer=customer,
                           recent_faults=recent_faults)


# ============================================
# Faults
# ============================================

@customer_bp.route('/faults')
@customer_login_required
def my_faults():
    """List customer's reported faults"""
    customer = g.customer
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = customer.reported_faults

    if status:
        query = query.filter_by(status=status)

    faults = query.order_by(Fault.reported_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('customer/my_faults.html', faults=faults, customer=customer, status=status)


@customer_bp.route('/faults/report', methods=['GET', 'POST'])
@customer_login_required
def report_fault():
    """Report a new fault"""
    customer = g.customer

    if request.method == 'POST':
        connection_id = request.form.get('connection_id') or None
        fault_type = request.form.get('fault_type')
        description = request.form.get('description')
        location_description = request.form.get('location_description')
        severity = request.form.get('severity', 'medium')

        # Verify connection belongs to customer if specified
        if connection_id:
            connection = Connection.query.filter_by(
                connection_id=connection_id,
                customer_id=customer.customer_id
            ).first()
            if not connection:
                flash('Invalid connection selected.', 'danger')
                return redirect(url_for('customer.report_fault'))

        fault = Fault(
            connection_id=connection_id,
            fault_type=fault_type,
            description=description,
            location_description=location_description,
            reported_by_customer=customer.customer_id,
            severity=severity
        )

        try:
            db.session.add(fault)
            db.session.commit()

            # Create notification for customer
            notification = Notification(
                customer_id=customer.customer_id,
                title='Fault Reported',
                message=f'Your fault report (#{fault.fault_id}) has been received. We will investigate shortly.',
                notification_type='fault_update',
                reference_type='fault',
                reference_id=fault.fault_id
            )
            db.session.add(notification)
            db.session.commit()

            flash('Fault reported successfully! We will investigate shortly.', 'success')
            return redirect(url_for('customer.view_fault', fault_id=fault.fault_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error reporting fault: {str(e)}', 'danger')

    connections = customer.connections.filter_by(connection_status='active').all()
    return render_template('customer/report_fault.html', connections=connections, customer=customer)


@customer_bp.route('/faults/<int:fault_id>')
@customer_login_required
def view_fault(fault_id):
    """View fault details and updates"""
    customer = g.customer
    fault = Fault.query.filter_by(
        fault_id=fault_id,
        reported_by_customer=customer.customer_id
    ).first_or_404()

    updates = fault.updates.order_by(FaultUpdate.update_date.desc()).all()

    return render_template('customer/view_fault.html', fault=fault, updates=updates, customer=customer)


# ============================================
# Service Requests
# ============================================

@customer_bp.route('/requests')
@customer_login_required
def my_requests():
    """List customer's service requests"""
    customer = g.customer
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = customer.service_requests

    if status:
        query = query.filter_by(status=status)

    requests_list = query.order_by(ServiceRequest.submitted_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('customer/my_requests.html', requests=requests_list, customer=customer, status=status)


@customer_bp.route('/requests/new', methods=['GET', 'POST'])
@customer_login_required
def new_request():
    """Submit a new service request"""
    customer = g.customer

    if request.method == 'POST':
        request_type = request.form.get('request_type')
        connection_id = request.form.get('connection_id') or None
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')

        # Verify connection belongs to customer if specified
        if connection_id:
            connection = Connection.query.filter_by(
                connection_id=connection_id,
                customer_id=customer.customer_id
            ).first()
            if not connection:
                flash('Invalid connection selected.', 'danger')
                return redirect(url_for('customer.new_request'))

        service_request = ServiceRequest(
            customer_id=customer.customer_id,
            connection_id=connection_id,
            request_type=request_type,
            description=description,
            priority=priority
        )

        try:
            db.session.add(service_request)
            db.session.commit()

            # Create notification for customer
            notification = Notification(
                customer_id=customer.customer_id,
                title='Service Request Submitted',
                message=f'Your service request (#{service_request.request_id}) has been submitted and is under review.',
                notification_type='service_update',
                reference_type='service_request',
                reference_id=service_request.request_id
            )
            db.session.add(notification)
            db.session.commit()

            flash('Service request submitted successfully!', 'success')
            return redirect(url_for('customer.view_request', request_id=service_request.request_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting request: {str(e)}', 'danger')

    connections = customer.connections.all()
    return render_template('customer/new_request.html', connections=connections, customer=customer)


@customer_bp.route('/requests/<int:request_id>')
@customer_login_required
def view_request(request_id):
    """View service request details"""
    customer = g.customer
    service_request = ServiceRequest.query.filter_by(
        request_id=request_id,
        customer_id=customer.customer_id
    ).first_or_404()

    return render_template('customer/view_request.html', request=service_request, customer=customer)


# ============================================
# Customer Support / Messaging
# ============================================

@customer_bp.route('/support')
@customer_login_required
def support():
    """Customer service message center"""
    customer = g.customer
    page = request.args.get('page', 1, type=int)

    # Get top-level messages (threads)
    messages = CustomerMessage.query.filter_by(
        customer_id=customer.customer_id,
        parent_message_id=None
    ).order_by(CustomerMessage.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('customer/support.html', messages=messages, customer=customer)


@customer_bp.route('/support/new', methods=['GET', 'POST'])
@customer_login_required
def new_message():
    """Send a new message to customer service"""
    customer = g.customer

    if request.method == 'POST':
        subject = request.form.get('subject')
        message_text = request.form.get('message')

        message = CustomerMessage(
            customer_id=customer.customer_id,
            subject=subject,
            message=message_text,
            is_from_customer=True
        )

        try:
            db.session.add(message)
            db.session.commit()
            flash('Message sent to customer service!', 'success')
            return redirect(url_for('customer.view_message', message_id=message.message_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error sending message: {str(e)}', 'danger')

    return render_template('customer/new_message.html', customer=customer)


@customer_bp.route('/support/<int:message_id>')
@customer_login_required
def view_message(message_id):
    """View message thread"""
    customer = g.customer

    # Get the top-level message
    message = CustomerMessage.query.filter_by(
        message_id=message_id,
        customer_id=customer.customer_id,
        parent_message_id=None
    ).first_or_404()

    # Mark unread replies as read
    unread_replies = CustomerMessage.query.filter_by(
        parent_message_id=message_id,
        is_from_customer=False,
        is_read=False
    ).all()
    for reply in unread_replies:
        reply.is_read = True
    db.session.commit()

    # Get all replies
    replies = message.replies.order_by(CustomerMessage.created_at.asc()).all()

    return render_template('customer/view_message.html', message=message, replies=replies, customer=customer)


@customer_bp.route('/support/<int:message_id>/reply', methods=['POST'])
@customer_login_required
def reply_message(message_id):
    """Reply to a message thread"""
    customer = g.customer

    # Verify original message belongs to customer
    original = CustomerMessage.query.filter_by(
        message_id=message_id,
        customer_id=customer.customer_id,
        parent_message_id=None
    ).first_or_404()

    message_text = request.form.get('message')

    reply = CustomerMessage(
        customer_id=customer.customer_id,
        subject=f"Re: {original.subject}",
        message=message_text,
        is_from_customer=True,
        parent_message_id=message_id
    )

    try:
        db.session.add(reply)
        db.session.commit()
        flash('Reply sent!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error sending reply: {str(e)}', 'danger')

    return redirect(url_for('customer.view_message', message_id=message_id))


# ============================================
# Notifications
# ============================================

@customer_bp.route('/notifications')
@customer_login_required
def notifications():
    """View all notifications"""
    customer = g.customer
    page = request.args.get('page', 1, type=int)

    notifications_list = Notification.query.filter_by(
        customer_id=customer.customer_id
    ).order_by(Notification.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # Mark all as read
    Notification.query.filter_by(
        customer_id=customer.customer_id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()

    return render_template('customer/notifications.html', notifications=notifications_list, customer=customer)


# ============================================
# Profile
# ============================================

@customer_bp.route('/profile')
@customer_login_required
def profile():
    """View customer profile"""
    customer = g.customer
    return render_template('customer/profile.html', customer=customer)


@customer_bp.route('/profile/update', methods=['POST'])
@customer_login_required
def update_profile():
    """Update customer profile (email and phone only)"""
    customer = g.customer

    email = request.form.get('email')
    phone = request.form.get('phone')

    if email:
        customer.email = email
    if phone:
        customer.phone = phone

    try:
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating profile: {str(e)}', 'danger')

    return redirect(url_for('customer.profile'))


@customer_bp.route('/profile/change-password', methods=['POST'])
@customer_login_required
def change_password():
    """Change customer password"""
    customer = g.customer

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not customer.check_password(current_password):
        flash('Current password is incorrect.', 'danger')
    elif new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
    elif len(new_password) < 6:
        flash('New password must be at least 6 characters long.', 'danger')
    else:
        customer.set_password(new_password)
        try:
            db.session.commit()
            flash('Password changed successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error changing password: {str(e)}', 'danger')

    return redirect(url_for('customer.profile'))
