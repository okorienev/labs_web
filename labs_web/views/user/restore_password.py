from flask.views import View
from flask import redirect, url_for, flash, request, render_template, current_app
from labs_web.extensions import RestorePasswordForm, User, db
import jwt


class RestorePassword(View):
    methods = ['GET', 'POST']

    def dispatch_request(self, *args, **kwargs):
        token = kwargs.get('token')
        if token:
            try:
                token_decoded = jwt.decode(token, current_app.config["SECRET_KEY"])
            except jwt.InvalidTokenError as exception:
                flash('Restoration token is not valid, try recreating the link')
                return redirect(url_for('auth.login'))
        user_id = token_decoded.get('id')
        form = RestorePasswordForm()
        if form.validate_on_submit() and request.method == 'POST':
            user = User.query.get(user_id)
            user.set_password(form.data.get('password'))
            db.session.commit()
            flash('password successfully changed')
            return redirect(url_for('auth.login'))
        if form.errors:
            for error in form.errors:
                flash(error)
        return render_template('user/restore_password.html', form=form)

