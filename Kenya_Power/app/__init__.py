"""
Application Factory for Kenya Power Management System
"""
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    """
    Application factory function

    Args:
        config_name: Configuration to use (development/production)

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register custom Jinja2 filters
    @app.template_filter('datetime')
    def datetime_filter(value, format='%B %d, %Y %H:%M'):
        """Format a datetime object or return current datetime if 'now' is passed."""
        if value == 'now' or value is None:
            return datetime.now().strftime(format)
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints (routes)
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.customers import customers_bp
    from app.routes.connections import connections_bp
    from app.routes.faults import faults_bp
    from app.routes.maintenance import maintenance_bp
    from app.routes.reports import reports_bp
    from app.routes.customer import customer_bp
    from app.routes.staff import staff_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(connections_bp, url_prefix='/connections')
    app.register_blueprint(faults_bp, url_prefix='/faults')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(customer_bp, url_prefix='/portal')
    app.register_blueprint(staff_bp, url_prefix='/staff')

    return app