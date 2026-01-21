"""
Maintenance scheduling and management routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import MaintenanceSchedule, MaintenanceLog, User, Notification
from app import db
from app.utils.decorators import role_required
from datetime import datetime, timedelta

maintenance_bp = Blueprint('maintenance', __name__)


@maintenance_bp.route('/')
@login_required
def list_maintenance():
    """List all maintenance schedules"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    maintenance_type = request.args.get('type', '')

    query = MaintenanceSchedule.query

    if status:
        query = query.filter_by(status=status)
    if maintenance_type:
        query = query.filter_by(maintenance_type=maintenance_type)

    # For technicians, show only assigned maintenance
    if current_user.role == 'technician':
        query = query.filter_by(assigned_to=current_user.user_id)

    schedules = query.order_by(MaintenanceSchedule.scheduled_date.asc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('maintenance/list.html', schedules=schedules,
                           status=status, maintenance_type=maintenance_type)


@maintenance_bp.route('/calendar')
@login_required
def calendar():
    """Calendar view of maintenance schedules"""
    return render_template('maintenance/calendar.html')


@maintenance_bp.route('/api/events')
@login_required
def get_events():
    """API endpoint for calendar events"""
    start = request.args.get('start')
    end = request.args.get('end')

    query = MaintenanceSchedule.query.filter(
        MaintenanceSchedule.scheduled_date >= start,
        MaintenanceSchedule.scheduled_date <= end
    )

    if current_user.role == 'technician':
        query = query.filter_by(assigned_to=current_user.user_id)

    schedules = query.all()

    events = []
    colors = {
        'scheduled': '#3788d8',
        'in_progress': '#f39c12',
        'completed': '#27ae60',
        'cancelled': '#e74c3c',
        'postponed': '#9b59b6'
    }

    for schedule in schedules:
        events.append({
            'id': schedule.maintenance_id,
            'title': schedule.title,
            'start': schedule.scheduled_date.isoformat(),
            'backgroundColor': colors.get(schedule.status, '#3788d8'),
            'url': url_for('maintenance.view_maintenance', maintenance_id=schedule.maintenance_id)
        })

    return jsonify(events)


@maintenance_bp.route('/schedule', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'manager')
def schedule_maintenance():
    """Schedule new maintenance"""
    if request.method == 'POST':
        schedule = MaintenanceSchedule(
            title=request.form.get('title'),
            description=request.form.get('description'),
            maintenance_type=request.form.get('maintenance_type'),
            equipment_type=request.form.get('equipment_type'),
            equipment_id=request.form.get('equipment_id'),
            location_description=request.form.get('location_description'),
            location_coordinates=request.form.get('location_coordinates'),
            scheduled_date=datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%d').date(),
            scheduled_time=datetime.strptime(request.form.get('scheduled_time'), '%H:%M').time() if request.form.get(
                'scheduled_time') else None,
            estimated_duration=request.form.get('estimated_duration'),
            assigned_team=request.form.get('assigned_team'),
            assigned_to=request.form.get('assigned_to') or None,
            priority=request.form.get('priority', 'medium'),
            created_by=current_user.user_id
        )

        try:
            db.session.add(schedule)
            db.session.commit()

            # Notify assigned technician
            if schedule.assigned_to:
                notification = Notification(
                    user_id=schedule.assigned_to,
                    title='New Maintenance Assignment',
                    message=f'You have been assigned maintenance: {schedule.title} scheduled for {schedule.scheduled_date}',
                    notification_type='maintenance_reminder',
                    reference_type='maintenance',
                    reference_id=schedule.maintenance_id
                )
                db.session.add(notification)
                db.session.commit()

            flash('Maintenance scheduled successfully!', 'success')
            return redirect(url_for('maintenance.view_maintenance', maintenance_id=schedule.maintenance_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling maintenance: {str(e)}', 'danger')

    technicians = User.query.filter_by(role='technician', is_active=True).all()
    return render_template('maintenance/schedule.html', technicians=technicians)


@maintenance_bp.route('/<int:maintenance_id>')
@login_required
def view_maintenance(maintenance_id):
    """View maintenance details"""
    schedule = MaintenanceSchedule.query.get_or_404(maintenance_id)
    logs = schedule.logs.order_by(MaintenanceLog.log_date.desc()).all()

    return render_template('maintenance/view.html', schedule=schedule, logs=logs)


@maintenance_bp.route('/<int:maintenance_id>/update-status', methods=['POST'])
@login_required
def update_maintenance_status(maintenance_id):
    """Update maintenance status"""
    schedule = MaintenanceSchedule.query.get_or_404(maintenance_id)
    new_status = request.form.get('status')

    schedule.status = new_status

    if new_status == 'completed':
        schedule.completion_date = datetime.utcnow()
        schedule.completion_notes = request.form.get('notes', '')

    try:
        db.session.commit()
        flash(f'Maintenance status updated to {new_status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')

    return redirect(url_for('maintenance.view_maintenance', maintenance_id=maintenance_id))


@maintenance_bp.route('/<int:maintenance_id>/log', methods=['POST'])
@login_required
@role_required('admin', 'manager', 'technician')
def add_maintenance_log(maintenance_id):
    """Add maintenance log entry"""
    schedule = MaintenanceSchedule.query.get_or_404(maintenance_id)

    log = MaintenanceLog(
        maintenance_id=maintenance_id,
        logged_by=current_user.user_id,
        work_performed=request.form.get('work_performed'),
        parts_used=request.form.get('parts_used'),
        issues_found=request.form.get('issues_found'),
        recommendations=request.form.get('recommendations'),
        actual_duration=request.form.get('actual_duration')
    )

    try:
        db.session.add(log)
        db.session.commit()
        flash('Maintenance log added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding log: {str(e)}', 'danger')

    return redirect(url_for('maintenance.view_maintenance', maintenance_id=maintenance_id))


from flask import jsonify