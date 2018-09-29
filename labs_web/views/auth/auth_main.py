from flask import Blueprint, g, redirect, url_for, current_app, request
from flask_login import current_user, login_required, logout_user
from . import Login


auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth')
auth.add_url_rule('/login/', view_func=Login.as_view(name='login'))


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/logout/')
@login_required
def logout():
    current_app.logger.info("{} logged out from addr {}".format(current_user.username,
                                                                request.remote_addr))
    logout_user()
    return redirect(url_for('auth.login'))

