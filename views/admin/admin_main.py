from flask import Blueprint, abort, render_template
from flask_login import current_user


admin = Blueprint(name='admin',
                  import_name=__name__,
                  url_prefix='/admin',)


@admin.before_request
def i_am_admin():
    if not current_user.role == 3:
        abort(404)


@admin.route('/home/')
def admin_home():
    return render_template('admin/index.html')
