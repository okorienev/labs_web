from flask import Blueprint, render_template
from flask_login import login_required
tutor = Blueprint('tutor',
                  __name__,
                  url_prefix='/tutor')


@tutor.route('/home/')
@login_required
def tutor_home():
    return render_template('tutor_home.html')
