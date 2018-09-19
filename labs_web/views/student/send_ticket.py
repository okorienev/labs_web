from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import Tickets, SendTicketForm, Course
from flask import request, flash, render_template, redirect, url_for
from datetime import datetime


class SendTicket(View):
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        form = SendTicketForm()
        form.course.choices = [(course.course_id, course.course_name) for course in current_user.group[0].courses]
        if request.method == "POST" and form.validate_on_submit():
            ticket = Tickets.insert_one({
                'author': {'id': current_user.id,
                           'name': current_user.name,
                           'group': current_user.group[0].name},
                'course': {'id': form.data.get('course'),
                           'name': Course.query.get(form.data.get('course')).course_name},
                'topic': form.data.get('topic'),
                'body': form.data.get('body'),
                'sent': datetime.utcnow()
            })
            flash('ticket {} registered'.format(ticket.inserted_id))
            return redirect(url_for('student.student_home'))
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)
        return render_template('student/send_ticket.html',
                               form=form)
