"""
Kenya Power Electrical Systems Management Application
Main entry point
"""
from app import create_app, db
from app.models import User

app = create_app('development')


@app.shell_context_processor
def make_shell_context():
    """Add database and models to shell context"""
    return {'db': db, 'User': User}


@app.cli.command()
def create_admin():
    """Create admin user"""
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@kenyapower.co.ke',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created successfully!')
        else:
            print('Admin user already exists.')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)