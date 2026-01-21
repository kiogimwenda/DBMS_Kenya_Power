"""
Main routes for Kenya Power Management System
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Customer, Connection, Fault, MaintenanceSchedule, ServiceRequest
from sqlalchemy import func
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with statistics"""
    # Get statistics
    stats = {
        'total_customers': Customer.query.filter_by(is_active=True).count(),
        'active_connections': Connection.query.filter_by(connection_status='active').count(),
        'pending_faults': Fault.query.filter(
            Fault.status.in_(['reported', 'acknowledged', 'assigned', 'in_progress'])).count(),
        'scheduled_maintenance': MaintenanceSchedule.query.filter_by(status='scheduled').count(),
        'pending_requests': ServiceRequest.query.filter(
            ServiceRequest.status.in_(['submitted', 'under_review'])).count()
    }

    # Recent faults
    recent_faults = Fault.query.order_by(Fault.reported_date.desc()).limit(5).all()

    # Upcoming maintenance
    upcoming_maintenance = MaintenanceSchedule.query.filter(
        MaintenanceSchedule.scheduled_date >= datetime.now().date()
    ).order_by(MaintenanceSchedule.scheduled_date).limit(5).all()

    # Fault statistics for chart
    thirty_days_ago = datetime.now() - timedelta(days=30)
    fault_stats = Fault.query.filter(Fault.reported_date >= thirty_days_ago).all()

    return render_template('dashboard.html',
                           stats=stats,
                           recent_faults=recent_faults,
                           upcoming_maintenance=upcoming_maintenance)