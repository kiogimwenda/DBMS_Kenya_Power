"""
Connection management routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Connection, Customer
from app import db
from app.utils.decorators import role_required
from datetime import datetime

connections_bp = Blueprint('connections', __name__)


@connections_bp.route('/')
@login_required
def list_connections():
    """List all connections"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')

    query = Connection.query

    if status:
        query = query.filter_by(connection_status=status)

    if search:
        query = query.filter(
            (Connection.meter_number.contains(search)) |
            (Connection.transformer_id.contains(search))
        )

    connections = query.order_by(Connection.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('connections/list.html', connections=connections, status=status, search=search)


@connections_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'manager', 'technician')
def add_connection():
    """Add new connection"""
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')

        # Generate meter number
        last_conn = Connection.query.order_by(Connection.connection_id.desc()).first()
        new_id = (last_conn.connection_id + 1) if last_conn else 1
        county_code = request.form.get('county_code', 'NAI')
        meter_number = f"MTR-{county_code}-{new_id:06d}"

        connection = Connection(
            customer_id=customer_id,
            meter_number=meter_number,
            connection_type=request.form.get('connection_type'),
            load_capacity=request.form.get('load_capacity'),
            installation_date=datetime.strptime(request.form.get('installation_date'),
                                                '%Y-%m-%d').date() if request.form.get('installation_date') else None,
            connection_status=request.form.get('connection_status', 'pending'),
            location_coordinates=request.form.get('location_coordinates'),
            transformer_id=request.form.get('transformer_id'),
            feeder_line=request.form.get('feeder_line')
        )

        try:
            db.session.add(connection)
            db.session.commit()
            flash(f'Connection {meter_number} created successfully!', 'success')
            return redirect(url_for('connections.view_connection', connection_id=connection.connection_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating connection: {str(e)}', 'danger')

    customers = Customer.query.filter_by(is_active=True).all()
    return render_template('connections/add.html', customers=customers)


@connections_bp.route('/<int:connection_id>')
@login_required
def view_connection(connection_id):
    """View connection details"""
    connection = Connection.query.get_or_404(connection_id)
    faults = connection.faults.order_by(Fault.reported_date.desc()).limit(5).all()

    return render_template('connections/view.html', connection=connection, faults=faults)


@connections_bp.route('/<int:connection_id>/status', methods=['POST'])
@login_required
@role_required('admin', 'manager', 'technician')
def update_status(connection_id):
    """Update connection status"""
    connection = Connection.query.get_or_404(connection_id)
    new_status = request.form.get('status')

    connection.connection_status = new_status

    try:
        db.session.commit()
        flash(f'Connection status updated to {new_status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')

    return redirect(url_for('connections.view_connection', connection_id=connection_id))


from app.models import Fault