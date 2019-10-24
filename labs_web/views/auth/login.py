from flask import request, redirect, url_for, render_template, flash, current_app
from flask_login import login_user, current_user
from flask.views import View
from flask_mail import Message
from labs_web.extensions import LoginForm, User, mail, celery, redis_conn, redis_get_int_or_none
from labs_web import app


@celery.task(ignore_result=True)
def notify_user_on_failed_attempt(user_id: int, ip: str):
    """
    notify user when somebody failed to attempt with his username
    :param user_id:
    :param ip:
    """
    with app.app_context():
        user = User.query.get(user_id)
        msg = Message()
        msg.sender = current_app.config['MAIL_SENDER']
        msg.recipients = [user.email]
        msg.html = render_template('mail/login_failed.html',
                                   user=user,
                                   ip=ip,
                                   attempts_username=current_app.config['LOGIN_ATTEMPT_USERNAME'],
                                   attempts_ip=current_app.config['LOGIN_ATTEMPT_IP'],
                                   login_delay=current_app.config['LOGIN_TIMEOUT'])
        mail.send(msg)


class Login(View):
    methods = ["GET", "POST"]

    @staticmethod
    def _may_attempt_to_authenticate(username: str, ip: str) -> bool:
        """
        :param username: username with which person is trying to log in
        :param ip: address from which person is trying to log in
        :return: True if person has attempts left, False otherwise
        """
        attempts_ip = redis_get_int_or_none(ip)
        attempts_username = redis_get_int_or_none(username)
        if ((attempts_username and attempts_username >= current_app.config['LOGIN_ATTEMPT_USERNAME']) or
                (attempts_ip and attempts_ip >= current_app.config['LOGIN_ATTEMPT_IP'])):
            return False
        return True

    @staticmethod
    def _login_attempt_failed(username: str, ip: str, user: User) -> None:
        """
        put failed attempts to redis, log with app logger
        :param username: username with which person failed to log in
        :param ip: address from which person failed to log in
        """
        current_app.logger.info("{} failed to log in from address: {}".format(
            user.username if user else "unknown user",
            request.remote_addr))
        flash('Login/password incorrect')

        username_attempts = redis_get_int_or_none(username)
        if not username_attempts:
            redis_conn.set(username, 1, ex=current_app.config['LOGIN_TIMEOUT'])
        else:
            redis_conn.incr(username)

        ip_attempt = redis_get_int_or_none(ip)
        if not ip_attempt:
            redis_conn.set(ip, 1, ex=current_app.config['LOGIN_TIMEOUT'])
        else:
            redis_conn.incr(ip)
        if ((username_attempts and username_attempts >= current_app.config['LOGIN_ATTEMPT_USERNAME']) or
                (ip_attempt and ip_attempt >= current_app.config['LOGIN_ATTEMPT_IP'])):
            if user:
                notify_user_on_failed_attempt.delay(user.id, request.remote_addr)

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
            if self._may_attempt_to_authenticate(request.form.get('username'),
                                                 request.remote_addr):
                user = User.query.filter_by(username=request.form.get('username')).first()
                if Login._user_can_be_logged_in(user, form.data.get('password')):
                    login_user(user, remember=request.form.get('remember_me'))
                    current_app.logger.info("{} logged in successfully from address: {}".format(user.username,
                                                                                                request.remote_addr))
                    return Login._make_homepage_redirects(user)
                else:
                    self._login_attempt_failed(request.form.get('username'),
                                               request.remote_addr,
                                               user)
                    return redirect(request.url)
            else:
                flash("You have to wait before trying to log in")
        return render_template('auth/login.html', form=form)
