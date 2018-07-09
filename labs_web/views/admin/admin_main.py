from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from .import AddGroup


admin = Blueprint(name='admin',
                  import_name=__name__,
                  url_prefix='/admin',)


@admin.before_request
@login_required
def i_am_admin():
    if current_user.role != 3:  # should be changed to query in large app with many roles but not necessary in this case
        abort(404)


@admin.route('/home/')
@login_required
def admin_home():
    return render_template('admin/admin_home.html')
