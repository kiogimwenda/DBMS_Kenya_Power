"""
Fault reporting and management routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Fault, FaultUpdate, Connection, Customer, User, Notification
from app import db
from app.utils.decorators import role_required
from datetime import datetime

faults_bp = Blueprint('faults', __name__)


@faults_bp.route('/')
@login_required
def list_faults():
    """List all faults"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    severity = request.args.get('severity', '')
    fault_type = request.args.get('fault_type', '')

    query = Fault.query

    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    if fault_type:
        query = query.filter_by(fault_type=fault_type)

    # For technicians, show only assigned faults
    if current_user.role == 'technician':
        query = query.filter(
            (Fault.assigned_to == current_user.user_id) |
            (Fault.status == 'reported')
        )

    faults = query.order_by(Fault.reported_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('faults/list.html', faults=faults,
                           status=status, severity=severity, fault_type=fault_type)


@faults_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report_fault():
    """Report a new fault"""
    if request.method == 'POST':
        fault = Fault(
            connection_id=request.form.get('connection_id') or None,
            fault_type=request.form.get('fault_type'),
            description=request.form.get('description'),
            location_description=request.form.get('location_description'),
            location_coordinates=request.form.get('location_coordinates'),
            reported_by_user=current_user.user_id,
            severity=request.form.get('severity', 'medium'),
            affected_customers=request.form.get('affected_customers', 1)
        )

        try:
            db.session.add(fault)
            db.session.commit()

            # Create notification for managers
            managers = User.query.filter_by(role='manager', is_active=True).all()
            for manager in managers:
                notification = Notification(
                    user_id=manager.user_id,
                    title='New Fault Reported',
                    message=f'A new {fault.fault_type} fault has been reported. Severity: {fault.severity}',
                    notification_type='fault_update',
                    reference_type='fault',
                    reference_id=fault.fault_id
                )
                db.session.add(notification)
            db.session.commit()

            flash('Fault reported successfully!', 'success')
            return redirect(url_for('faults.view_fault', fault_id=fault.fault_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error reporting fault: {str(e)}', 'danger')

    connections = Connection.query.filter_by(connection_status='active').all()
    return render_template('faults/report.html', connections=connections)


@faults_bp.route('/<int:fault_id>')
@login_required
def view_fault(fault_id):
    """View fault details"""
    fault = Fault.query.get_or_404(fault_id)
    updates = fault.updates.order_by(FaultUpdate.update_date.desc()).all()
    technicians = User.query.filter_by(role='technician', is_active=True).all()

    return render_template('faults/view.html', fault=fault, updates=updates, technicians=technicians)


@faults_bp.route('/<int:fault_id>/assign', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def assign_fault(fault_id):
    """Assign fault to technician"""
    fault = Fault.query.get_or_404(fault_id)
    technician_id = request.form.get('technician_id')

    previous_status = fault.status
    fault.assigned_to = technician_id
    fault.assigned_date = datetime.utcnow()
    fault.status = 'assigned'

    # Log the update
    update = FaultUpdate(
        fault_id=fault_id,
        updated_by=current_user.user_id,
        update_type='assignment',
        previous_status=previous_status,
        new_status='assigned',
        notes=f'Assigned to technician ID: {technician_id}'
    )

    # Notify technician
    notification = Notification(
        user_id=technician_id,
        title='New Fault Assignment',
        message=f'You have been assigned fault #{fault_id}: {fault.fault_type}',
        notification_type='fault_update',
        reference_type='fault',
        reference_id=fault_id
    )

    try:
        db.session.add(update)
        db.session.add(notification)
        db.session.commit()
        flash('Fault assigned successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error assigning fault: {str(e)}', 'danger')

    return redirect(url_for('faults.view_fault', fault_id=fault_id))


@faults_bp.route('/<int:fault_id>/update-status', methods=['POST'])
@login_required
def update_fault_status(fault_id):
    """Update fault status"""
    fault = Fault.query.get_or_404(fault_id)
    new_status = request.form.get('status')
    notes = request.form.get('notes', '')

    previous_status = fault.status
    fault.status = new_status

    if new_status in ['resolved', 'closed']:
        fault.resolution_date = datetime.utcnow()
        fault.resolution_notes = notes

    # Log the update
    update = FaultUpdate(
        fault_id=fault_id,
        updated_by=current_user.user_id,
        update_type='status_change',
        previous_status=previous_status,
        new_status=new_status,
        notes=notes
    )

    try:
        db.session.add(update)
        db.session.commit()
        flash(f'Fault status updated to {new_status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')

    return redirect(url_for('faults.view_fault', fault_id=fault_id))


@faults_bp.route('/<int:fault_id>/add-note', methods=['POST'])
@login_required
def add_fault_note(fault_id):
    """Add note to fault"""
    fault = Fault.query.get_or_404(fault_id)
    notes = request.form.get('notes')

    update = FaultUpdate(
        fault_id=fault_id,
        updated_by=current_user.user_id,
        update_type='note',
        notes=notes
    )

    try:
        db.session.add(update)
        db.session.commit()
        flash('Note added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding note: {str(e)}', 'danger')

    return redirect(url_for('faults.view_fault', fault_id=fault_id))