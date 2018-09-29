from flask import request, redirect, url_for, render_template, flash, current_app
from flask_login import login_user, current_user
from flask.views import View
from labs_web.extensions import LoginForm, User


class Login(View):
    methods = ["GET", "POST"]

    @staticmethod
    def _make_homepage_redirects(user: User):
        """redirects depending on role"""
        if user.role == 1:
            return redirect((url_for('student.student_home')))
        if user.role == 2:
            return redirect(url_for('tutor.tutor_home'))
        if user.role == 3:
            return redirect(url_for('admin.index'))

    @staticmethod
    def _user_can_be_logged_in(user: User, password: str):
        """check for user existing and for correct password"""
        if not user:
            return False
        if not user.check_password(password):
            return False
        return True

    def dispatch_request(self):
        form = LoginForm()
        if current_user.is_authenticated:
            return Login._make_homepage_redirects(current_user)
        if request.method == "POST" and form.validate_on_submit():
            user = User.query.filter_by(username=request.form.get('username')).first()
            if Login._user_can_be_logged_in(user, form.data.get('password')):
                login_user(user, remember=request.form.get('remember_me'))
                current_app.logger.info("{} logged in successfully from address: {}".format(user.username,
                                                                                            request.remote_addr))
                return Login._make_homepage_redirects(user)
            else:
                flash('Login/password incorrect')
                current_app.logger.info("{} failed to log in from address: {}".format(
                    user.username if user else "uknown user",
                    request.remote_addr))
                return redirect(request.url)
        return render_template('auth/login.html', form=form)
