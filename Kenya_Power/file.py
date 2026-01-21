from app import create_app, db
from app.models import User

app = create_app('development')
with app.app_context():
    User.query.filter_by(username='admin').delete()
    db.session.commit()

    admin = User(
        username='admin',
        email='admin@kenyapower.co.ke',
        full_name='System Administrator',
        phone='+254700000001',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Admin created!')
    print('Username: admin')
    print('Password: admin123')