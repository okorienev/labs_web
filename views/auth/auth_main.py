from flask import Blueprint, request, redirect, url_for, render_template, abort, g
from models import User
from flask_login import login_user, current_user, login_required
from forms import LoginForm
auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user.check_password(request.form.get('password')):
            login_user(user, remember=request.form.get('remember_me'))
            if user.role == 1:
                return redirect((url_for('student.send_report')))
            if user.role == 2:
                return redirect(url_for('tutor.tutor_home'))
        else:
            abort(401)
    return render_template('login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    login_user(current_user)

