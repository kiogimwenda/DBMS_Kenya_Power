"""
Database initialization script
"""
from app import create_app, db
from app.models import User

app = create_app('development')

with app.app_context():
    # Create all tables
    db.create_all()

    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@kenyapower.co.ke',
            full_name='System Administrator',
            phone='+254700000001',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Add sample users
        users_data = [
            ('manager1', 'manager@kenyapower.co.ke', 'James Mwangi', '+254700000002', 'manager', 'password123'),
            ('tech1', 'technician1@kenyapower.co.ke', 'Peter Ochieng', '+254700000003', 'technician', 'password123'),
            ('tech2', 'technician2@kenyapower.co.ke', 'Mary Wanjiku', '+254700000004', 'technician', 'password123'),
            ('cs_agent1', 'csagent1@kenyapower.co.ke', 'Sarah Kimani', '+254700000005', 'customer_service',
             'password123'),
        ]

        for username, email, full_name, phone, role, password in users_data:
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                role=role
            )
            user.set_password(password)
            db.session.add(user)

        db.session.commit()
        print('Database initialized with admin and sample users!')
        print('\nDefault Login Credentials:')
        print('Username: admin')
        print('Password: admin123')
    else:
        print('Database already initialized.')