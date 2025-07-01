from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main_bp
from ..models import User, FSE, Assessment # etc
from .. import db

@main_bp.route('/')
@main_bp.route('/index')
# @login_required # Decide if index needs login
def index():
    # This could be a generic landing page or redirect to a dashboard based on role
    # if current_user.is_authenticated:
    #     if current_user.role == 'admin':
    #         return redirect(url_for('admin.dashboard')) # Assuming admin blueprint
    #     elif current_user.role == 'assessor':
    #         return redirect(url_for('assessor.dashboard')) # Assuming assessor blueprint
    #     elif current_user.role == 'fse_owner':
    #         return redirect(url_for('fse_owner.dashboard')) # Assuming fse_owner blueprint
    # return render_template('main/index.html', title='Home')
    return "Main Index Page Placeholder - Welcome!"

# Example protected route
@main_bp.route('/profile')
@login_required
def profile():
    # return render_template('main/profile.html', title='Profile')
    return f"User Profile Page for {current_user.username} (Role: {current_user.role})"
