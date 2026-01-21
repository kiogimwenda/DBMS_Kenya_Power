"""
Customer management routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Customer, Connection
from app import db
from app.utils.decorators import role_required

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/')
@login_required
def list_customers():
    """List all customers"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Customer.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            (Customer.account_number.contains(search)) |
            (Customer.first_name.contains(search)) |
            (Customer.last_name.contains(search)) |
            (Customer.phone.contains(search))
        )

    customers = query.order_by(Customer.registration_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('customers/list.html', customers=customers, search=search)


@customers_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'manager', 'customer_service')
def add_customer():
    """Add new customer"""
    if request.method == 'POST':
        # Generate account number
        last_customer = Customer.query.order_by(Customer.customer_id.desc()).first()
        new_id = (last_customer.customer_id + 1) if last_customer else 1
        account_number = f"KP-{datetime.now().year}-{new_id:04d}"

        customer = Customer(
            account_number=account_number,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            id_number=request.form.get('id_number'),
            address=request.form.get('address'),
            county=request.form.get('county'),
            town=request.form.get('town'),
            postal_code=request.form.get('postal_code'),
            customer_type=request.form.get('customer_type')
        )

        try:
            db.session.add(customer)
            db.session.commit()
            flash(f'Customer {account_number} created successfully!', 'success')
            return redirect(url_for('customers.view_customer', customer_id=customer.customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating customer: {str(e)}', 'danger')

    return render_template('customers/add.html')


@customers_bp.route('/<int:customer_id>')
@login_required
def view_customer(customer_id):
    """View customer details"""
    customer = Customer.query.get_or_404(customer_id)
    connections = customer.connections.all()
    service_requests = customer.service_requests.order_by(ServiceRequest.submitted_date.desc()).limit(5).all()

    return render_template('customers/view.html',
                           customer=customer,
                           connections=connections,
                           service_requests=service_requests)


@customers_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'manager', 'customer_service')
def edit_customer(customer_id):
    """Edit customer details"""
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'POST':
        customer.first_name = request.form.get('first_name')
        customer.last_name = request.form.get('last_name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        customer.county = request.form.get('county')
        customer.town = request.form.get('town')
        customer.postal_code = request.form.get('postal_code')
        customer.customer_type = request.form.get('customer_type')

        try:
            db.session.commit()
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customers.view_customer', customer_id=customer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating customer: {str(e)}', 'danger')

    return render_template('customers/edit.html', customer=customer)


from datetime import datetime
from app.models import ServiceRequest