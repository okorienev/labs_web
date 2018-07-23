from flask import request, url_for, flash, redirect, render_template, current_app
from flask.views import View
from labs_web.extensions import ForgotPasswordForm, User, celery, mail
from labs_web.config import Config
from flask_mail import Message
from labs_web import app
import jwt
import time


@celery.task(ignore_result=True)
def forgot_password(user_id: int, email: str, name: str, url_no_token: str):
    """
    background task to generate restoration link and send it to the student
    """
    with app.test_request_context('/user/forgot/'):
        token = jwt.encode(
            {'id': user_id,
             'exp': time.time() + 60 * 60 * 12},
            current_app.config["SECRET_KEY"],
            algorithm='HS256'
        )
        msg = Message()
        msg.sender = 'labs.web.notifications'
        msg.recipients = [email]
        msg.subject = 'Restore password'
        msg.html = render_template('mail/forgot_password.html',
                                   name=name,
                                   url=url_no_token.replace('token', token.decode()))
        mail.send(msg)


class ForgotPassword(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = ForgotPasswordForm()
        if request.method == 'POST' and form.validate_on_submit():
            user = User.query.filter_by(email=form.data.get('email')).first()
            if user:
                forgot_password.delay(user.id,
                                      user.email,
                                      user.name,
                                      url_for('user.restore-password', token='token', _external=True))
                flash('restoration link will be sent to your email')
                return redirect(url_for('auth.login'))
            else:
                flash('User not found')
                return redirect(request.url)
        return render_template('user/forgot_password.html', form=form)

