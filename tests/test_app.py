"""
Test suite for Kenya Power Management System
"""
import unittest
from app import create_app, db
from app.models import User, Customer, Connection, Fault, MaintenanceSchedule


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'


class TestBase(unittest.TestCase):
    """Base test class"""

    def setUp(self):
        self.app = create_app('default')
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.test_user = User(
            username='testuser',
            email='test@test.com',
            full_name='Test User',
            role='admin'
        )
        self.test_user.set_password('testpass')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username='testuser', password='testpass'):
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)


class TestAuth(TestBase):
    """Test authentication"""

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_success(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_login_failure(self):
        response = self.login('wronguser', 'wrongpass')
        self.assertIn(b'Invalid', response.data)

    def test_logout(self):
        self.login()
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)


class TestCustomer(TestBase):
    """Test customer management"""

    def test_customer_list(self):
        self.login()
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_add_customer(self):
        self.login()
        response = self.client.post('/customers/add', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+254711111111',
            'id_number': '12345678',
            'address': '123 Test Street',
            'county': 'Nairobi',
            'town': 'Nairobi CBD',
            'customer_type': 'residential'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        customer = Customer.query.filter_by(id_number='12345678').first()
        self.assertIsNotNone(customer)


class TestFault(TestBase):
    """Test fault management"""

    def test_fault_list(self):
        self.login()
        response = self.client.get('/faults/')
        self.assertEqual(response.status_code, 200)

    def test_report_fault(self):
        self.login()
        response = self.client.post('/faults/report', data={
            'fault_type': 'power_outage',
            'description': 'Test fault description',
            'location_description': 'Test location',
            'severity': 'medium',
            'affected_customers': 10
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        fault = Fault.query.filter_by(description='Test fault description').first()
        self.assertIsNotNone(fault)


class TestMaintenance(TestBase):
    """Test maintenance management"""

    def test_maintenance_list(self):
        self.login()
        response = self.client.get('/maintenance/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()