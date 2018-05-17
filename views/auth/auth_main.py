from flask import Blueprint, g
from flask_login import login_user, current_user, login_required
from views.auth.login import Login


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
    login_user(current_user)

