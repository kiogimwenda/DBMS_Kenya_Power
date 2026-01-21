
"""
Performance reporting routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import Fault, MaintenanceSchedule, Customer, Connection, ServiceRequest
from app import db
from app.utils.decorators import role_required
from sqlalchemy import func
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/')
@login_required
@role_required('admin', 'manager')
def index():
    """Reports dashboard"""
    return render_template('reports/index.html')


@reports_bp.route('/faults')
@login_required
@role_required('admin', 'manager')
def fault_reports():
    """Fault resolution reports"""
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    if request.args.get('start_date'):
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    if request.args.get('end_date'):
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

    # Fault statistics
    faults = Fault.query.filter(
        Fault.reported_date >= start_date,
        Fault.reported_date <= end_date
    ).all()

    total_faults = len(faults)
    resolved_faults = len([f for f in faults if f.status in ['resolved', 'closed']])

    # Average resolution time
    resolution_times = [f.resolution_time_hours for f in faults if f.resolution_time_hours]
    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0

    # Faults by type
    faults_by_type = db.session.query(
        Fault.fault_type, func.count(Fault.fault_id)
    ).filter(
        Fault.reported_date >= start_date,
        Fault.reported_date <= end_date
    ).group_by(Fault.fault_type).all()

    # Faults by severity
    faults_by_severity = db.session.query(
        Fault.severity, func.count(Fault.fault_id)
    ).filter(
        Fault.reported_date >= start_date,
        Fault.reported_date <= end_date
    ).group_by(Fault.severity).all()

    # Daily fault trend
    daily_faults = db.session.query(
        func.date(Fault.reported_date), func.count(Fault.fault_id)
    ).filter(
        Fault.reported_date >= start_date,
        Fault.reported_date <= end_date
    ).group_by(func.date(Fault.reported_date)).all()

    return render_template('reports/faults.html',
                           start_date=start_date,
                           end_date=end_date,
                           total_faults=total_faults,
                           resolved_faults=resolved_faults,
                           avg_resolution_time=round(avg_resolution_time, 2),
                           faults_by_type=faults_by_type,
                           faults_by_severity=faults_by_severity,
                           daily_faults=daily_faults)


@reports_bp.route('/maintenance')
@login_required
@role_required('admin', 'manager')
def maintenance_reports():
    """Maintenance activity reports"""
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    if request.args.get('start_date'):
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
    if request.args.get('end_date'):
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

    # Maintenance statistics
    schedules = MaintenanceSchedule.query.filter(
        MaintenanceSchedule.scheduled_date >= start_date.date(),
        MaintenanceSchedule.scheduled_date <= end_date.date()
    ).all()

    total_scheduled = len(schedules)
    completed = len([s for s in schedules if s.status == 'completed'])
    in_progress = len([s for s in schedules if s.status == 'in_progress'])
    cancelled = len([s for s in schedules if s.status == 'cancelled'])

    # By type
    by_type = db.session.query(
        MaintenanceSchedule.maintenance_type, func.count(MaintenanceSchedule.maintenance_id)
    ).filter(
        MaintenanceSchedule.scheduled_date >= start_date.date(),
        MaintenanceSchedule.scheduled_date <= end_date.date()
    ).group_by(MaintenanceSchedule.maintenance_type).all()

    # By equipment
    by_equipment = db.session.query(
        MaintenanceSchedule.equipment_type, func.count(MaintenanceSchedule.maintenance_id)
    ).filter(
        MaintenanceSchedule.scheduled_date >= start_date.date(),
        MaintenanceSchedule.scheduled_date <= end_date.date()
    ).group_by(MaintenanceSchedule.equipment_type).all()

    return render_template('reports/maintenance.html',
                           start_date=start_date,
                           end_date=end_date,
                           total_scheduled=total_scheduled,
                           completed=completed,
                           in_progress=in_progress,
                           cancelled=cancelled,
                           by_type=by_type,
                           by_equipment=by_equipment)


@reports_bp.route('/performance')
@login_required
@role_required('admin', 'manager')
def performance_dashboard():
    """Overall performance dashboard"""
    # Current statistics
    stats = {
        'total_customers': Customer.query.filter_by(is_active=True).count(),
        'active_connections': Connection.query.filter_by(connection_status='active').count(),
        'suspended_connections': Connection.query.filter_by(connection_status='suspended').count(),
        'total_faults_month': Fault.query.filter(
            Fault.reported_date >= datetime.now() - timedelta(days=30)
        ).count(),
        'resolved_faults_month': Fault.query.filter(
            Fault.reported_date >= datetime.now() - timedelta(days=30),
            Fault.status.in_(['resolved', 'closed'])
        ).count(),
        'maintenance_completed_month': MaintenanceSchedule.query.filter(
            MaintenanceSchedule.completion_date >= datetime.now() - timedelta(days=30)
        ).count(),
        'pending_requests': ServiceRequest.query.filter(
            ServiceRequest.status.in_(['submitted', 'under_review'])
        ).count()
    }

    # Calculate percentages
    if stats['total_faults_month'] > 0:
        stats['resolution_rate'] = round(
            (stats['resolved_faults_month'] / stats['total_faults_month']) * 100, 1
        )
    else:
        stats['resolution_rate'] = 100

    return render_template('reports/performance.html', stats=stats)


@reports_bp.route('/api/chart-data/<chart_type>')
@login_required
@role_required('admin', 'manager')
def get_chart_data(chart_type):
    """API endpoint for chart data"""
    days = int(request.args.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)

    if chart_type == 'faults_trend':
        data = db.session.query(
            func.date(Fault.reported_date), func.count(Fault.fault_id)
        ).filter(Fault.reported_date >= start_date).group_by(
            func.date(Fault.reported_date)
        ).all()

        return jsonify({
            'labels': [str(d[0]) for d in data],
            'values': [d[1] for d in data]
        })

    elif chart_type == 'faults_by_type':
        data = db.session.query(
            Fault.fault_type, func.count(Fault.fault_id)
        ).filter(Fault.reported_date >= start_date).group_by(Fault.fault_type).all()

        return jsonify({
            'labels': [d[0].replace('_', ' ').title() for d in data],
            'values': [d[1] for d in data]
        })

    return jsonify({'error': 'Invalid chart type'})