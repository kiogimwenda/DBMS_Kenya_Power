"""
Database Models for Kenya Power Management System
"""
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Will store plain password now
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum('admin', 'manager', 'technician', 'customer_service'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assigned_faults = db.relationship('Fault', foreign_keys='Fault.assigned_to', backref='technician', lazy='dynamic')
    assigned_maintenance = db.relationship('MaintenanceSchedule', foreign_keys='MaintenanceSchedule.assigned_to', backref='technician', lazy='dynamic')

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        """Store password directly (plain text - for demo only)"""
        self.password = password

    def check_password(self, password):
        """Check password directly (plain text comparison)"""
        return self.password == password


class Customer(db.Model):
    """Customer model"""
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    county = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(10))
    customer_type = db.Column(db.Enum('residential', 'commercial', 'industrial'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Portal authentication fields
    password = db.Column(db.String(255))
    portal_registered = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    # Relationships
    connections = db.relationship('Connection', backref='customer', lazy='dynamic')
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy='dynamic')
    reported_faults = db.relationship('Fault', foreign_keys='Fault.reported_by_customer', backref='reporting_customer', lazy='dynamic')
    messages = db.relationship('CustomerMessage', backref='customer', lazy='dynamic')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        """Store password (plain text for demo)"""
        self.password = password

    def check_password(self, password):
        """Check password (plain text comparison)"""
        return self.password == password

    def __repr__(self):
        return f'<Customer {self.account_number}>'


class Connection(db.Model):
    """Electrical connection model"""
    __tablename__ = 'connections'

    connection_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    meter_number = db.Column(db.String(20), unique=True, nullable=False)
    connection_type = db.Column(db.Enum('single_phase', 'three_phase'), nullable=False)
    load_capacity = db.Column(db.Numeric(10, 2), nullable=False)
    installation_date = db.Column(db.Date)
    connection_status = db.Column(db.Enum('pending', 'active', 'suspended', 'disconnected'), default='pending')
    location_coordinates = db.Column(db.String(50))
    transformer_id = db.Column(db.String(20))
    feeder_line = db.Column(db.String(50))
    last_reading_date = db.Column(db.Date)
    last_reading_value = db.Column(db.Numeric(12, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    faults = db.relationship('Fault', backref='connection', lazy='dynamic')
    service_requests = db.relationship('ServiceRequest', backref='connection', lazy='dynamic')

    def __repr__(self):
        return f'<Connection {self.meter_number}>'


class Fault(db.Model):
    """Fault report model"""
    __tablename__ = 'faults'

    fault_id = db.Column(db.Integer, primary_key=True)
    connection_id = db.Column(db.Integer, db.ForeignKey('connections.connection_id'))
    fault_type = db.Column(db.Enum('power_outage', 'low_voltage', 'high_voltage', 'meter_fault', 'transformer_fault', 'line_fault', 'other'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location_description = db.Column(db.Text)
    location_coordinates = db.Column(db.String(50))
    reported_by_customer = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    reported_by_user = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    reported_date = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.Enum('low', 'medium', 'high', 'critical'), default='medium')
    status = db.Column(db.Enum('reported', 'acknowledged', 'assigned', 'in_progress', 'resolved', 'closed'), default='reported')
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    assigned_date = db.Column(db.DateTime)
    resolution_date = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    affected_customers = db.Column(db.Integer, default=1)

    # Relationships
    updates = db.relationship('FaultUpdate', backref='fault', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def resolution_time_hours(self):
        """Calculate resolution time in hours"""
        if self.resolution_date and self.reported_date:
            delta = self.resolution_date - self.reported_date
            return delta.total_seconds() / 3600
        return None

    def __repr__(self):
        return f'<Fault {self.fault_id}>'


class FaultUpdate(db.Model):
    """Fault update/progress tracking model"""
    __tablename__ = 'fault_updates'

    update_id = db.Column(db.Integer, primary_key=True)
    fault_id = db.Column(db.Integer, db.ForeignKey('faults.fault_id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    update_type = db.Column(db.Enum('status_change', 'assignment', 'note', 'resolution'), nullable=False)
    previous_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref='fault_updates')

    def __repr__(self):
        return f'<FaultUpdate {self.update_id}>'


class MaintenanceSchedule(db.Model):
    """Maintenance schedule model"""
    __tablename__ = 'maintenance_schedules'

    maintenance_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    maintenance_type = db.Column(db.Enum('preventive', 'corrective', 'emergency', 'inspection'), nullable=False)
    equipment_type = db.Column(db.Enum('transformer', 'feeder_line', 'meter', 'pole', 'substation', 'other'), nullable=False)
    equipment_id = db.Column(db.String(50))
    location_description = db.Column(db.Text, nullable=False)
    location_coordinates = db.Column(db.String(50))
    scheduled_date = db.Column(db.Date, nullable=False)
    scheduled_time = db.Column(db.Time)
    estimated_duration = db.Column(db.Integer)
    assigned_team = db.Column(db.String(100))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    status = db.Column(db.Enum('scheduled', 'in_progress', 'completed', 'cancelled', 'postponed'), default='scheduled')
    priority = db.Column(db.Enum('low', 'medium', 'high', 'critical'), default='medium')
    completion_date = db.Column(db.DateTime)
    completion_notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    logs = db.relationship('MaintenanceLog', backref='schedule', lazy='dynamic', cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_maintenance')

    def __repr__(self):
        return f'<MaintenanceSchedule {self.maintenance_id}>'


class MaintenanceLog(db.Model):
    """Maintenance log/work record model"""
    __tablename__ = 'maintenance_logs'

    log_id = db.Column(db.Integer, primary_key=True)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance_schedules.maintenance_id'), nullable=False)
    logged_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    work_performed = db.Column(db.Text, nullable=False)
    parts_used = db.Column(db.Text)
    issues_found = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    actual_duration = db.Column(db.Integer)
    log_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref='maintenance_logs')

    def __repr__(self):
        return f'<MaintenanceLog {self.log_id}>'


class ServiceRequest(db.Model):
    """Service request model"""
    __tablename__ = 'service_requests'

    request_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    connection_id = db.Column(db.Integer, db.ForeignKey('connections.connection_id'))
    request_type = db.Column(db.Enum('new_connection', 'upgrade', 'downgrade', 'relocation', 'name_change', 'disconnection', 'reconnection'), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('submitted', 'under_review', 'approved', 'in_progress', 'completed', 'rejected'), default='submitted')
    priority = db.Column(db.Enum('low', 'medium', 'high', 'urgent'), default='medium')
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_date = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)

    # Relationship
    assignee = db.relationship('User', backref='assigned_requests')

    def __repr__(self):
        return f'<ServiceRequest {self.request_id}>'


class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.Enum('fault_update', 'maintenance_reminder', 'service_update', 'system', 'alert'), nullable=False)
    reference_type = db.Column(db.String(50))
    reference_id = db.Column(db.Integer)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.notification_id}>'


class CustomerMessage(db.Model):
    """Customer service messaging model"""
    __tablename__ = 'customer_messages'

    message_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_from_customer = db.Column(db.Boolean, default=True)
    is_read = db.Column(db.Boolean, default=False)
    parent_message_id = db.Column(db.Integer, db.ForeignKey('customer_messages.message_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='customer_messages')
    replies = db.relationship('CustomerMessage', backref=db.backref('parent', remote_side=[message_id]), lazy='dynamic')

    def __repr__(self):
        return f'<CustomerMessage {self.message_id}>'