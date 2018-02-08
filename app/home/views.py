from flask import render_template, abort
from flask_login import login_required, current_user


from . import home


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():    
    # prevent non-admins from accessing the page          
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="DashBoard")


@home.route('/')
def homepage():
    """
    render the home page on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title="Dashboard")
