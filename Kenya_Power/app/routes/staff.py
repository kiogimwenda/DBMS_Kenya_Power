"""
Staff management routes - Admin only
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User
from app import db
from app.utils.decorators import role_required

staff_bp = Blueprint('staff', __name__)


@staff_bp.route('/')
@login_required
@role_required('admin')
def list_staff():
    """List all staff members (customer care agents and technicians)"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')

    query = User.query.filter(User.role.in_(['customer_service', 'technician']))

    if search:
        query = query.filter(
            (User.username.contains(search)) |
            (User.full_name.contains(search)) |
            (User.email.contains(search))
        )

    if role_filter:
        query = query.filter(User.role == role_filter)

    staff = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('staff/list.html', staff=staff, search=search, role_filter=role_filter)


@staff_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_staff():
    """Add new staff member (customer care agent or technician)"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        role = request.form.get('role')

        # Validation
        if not all([username, email, password, full_name, role]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('staff/add.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('staff/add.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('staff/add.html')

        if role not in ['customer_service', 'technician']:
            flash('Invalid role selected.', 'danger')
            return render_template('staff/add.html')

        # Check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('staff/add.html')

        # Check if email exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('staff/add.html')

        # Create new staff user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            role=role,
            is_active=True
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Staff member "{full_name}" created successfully!', 'success')
            return redirect(url_for('staff.list_staff'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating staff member: {str(e)}', 'danger')

    return render_template('staff/add.html')


@staff_bp.route('/<int:user_id>')
@login_required
@role_required('admin')
def view_staff(user_id):
    """View staff member details"""
    user = User.query.get_or_404(user_id)
    if user.role not in ['customer_service', 'technician']:
        flash('Staff member not found.', 'danger')
        return redirect(url_for('staff.list_staff'))

    return render_template('staff/view.html', user=user)


@staff_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_staff(user_id):
    """Edit staff member details"""
    user = User.query.get_or_404(user_id)
    if user.role not in ['customer_service', 'technician']:
        flash('Staff member not found.', 'danger')
        return redirect(url_for('staff.list_staff'))

    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.role = request.form.get('role')

        # Check if new email conflicts with existing
        existing_email = User.query.filter(User.email == user.email, User.user_id != user_id).first()
        if existing_email:
            flash('Email already in use by another user.', 'danger')
            return render_template('staff/edit.html', user=user)

        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('staff/edit.html', user=user)
            user.set_password(new_password)

        try:
            db.session.commit()
            flash('Staff member updated successfully!', 'success')
            return redirect(url_for('staff.view_staff', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating staff member: {str(e)}', 'danger')

    return render_template('staff/edit.html', user=user)


@staff_bp.route('/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@role_required('admin')
def toggle_status(user_id):
    """Activate or deactivate a staff member"""
    user = User.query.get_or_404(user_id)
    if user.role not in ['customer_service', 'technician']:
        flash('Staff member not found.', 'danger')
        return redirect(url_for('staff.list_staff'))

    user.is_active = not user.is_active
    status = 'activated' if user.is_active else 'deactivated'

    try:
        db.session.commit()
        flash(f'Staff member {user.full_name} has been {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')

    return redirect(url_for('staff.list_staff'))
