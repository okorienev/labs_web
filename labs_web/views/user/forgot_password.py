from flask import request, url_for, flash, redirect, render_template
from flask.views import View
from labs_web.extensions import ForgotPasswordForm, User, celery, mail
from labs_web.config import Config
from flask_mail import Message
from labs_web import app
import jwt
import time


@celery.task(ignore_result=True)
def forgot_password(user_id: int):
    """
    background task to generate restoration link and send it to the student
    """
    with app.app_context():
        user = User.query.get(user_id)
        token = jwt.encode(
            {'id': user.id,
             'exp': time.time() + 60 * 60 * 12},
            Config.SECRET_KEY,
            algorithm='HS256'
        )
        msg = Message()
        msg.sender = 'labs.web.notifications'
        msg.recipients = [user.email]
        msg.subject = 'Restore password'
        msg.html = render_template('mail/forgot_password.html',
                                   user=user,
                                   url=url_for('user.restore-password', token=token))
        print(msg.html)
        mail.send(msg)


class ForgotPassword(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = ForgotPasswordForm()
        if request.method == 'POST' and form.validate_on_submit():
            email = form.data.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                forgot_password.delay(user.id)
                flash('restoration link will be sent to your email')
                return redirect(url_for('auth.login'))
            else:
                flash('User not found')
                return redirect(request.url)
        return render_template('user/forgot_password.html', form=form)

