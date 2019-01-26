from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import AnswerTicketForm, Tickets, mongo_oid
from flask import request, flash, render_template, abort
from datetime import datetime


class AnswerTicket(View):
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            flash("invalid integer literal for page/no page provided")
            return abort(404)
        pages = Tickets.count({'course.id': {'$in': [course.course_id for course in
                                                     current_user.courses]},
                               'checked': {'$exists': False}})
        form = AnswerTicketForm()
        tickets = [i for i in Tickets.find({'course.id': {'$in': [course.course_id for course in
                                                                  current_user.courses]},
                                            'checked': {'$exists': False}})]
        form.selected_ticket.choices = [(str(ticket['_id']),
                                         "{} - {} ({}) {}".format(ticket['topic'],
                                                                  ticket['author']['name'],
                                                                  ticket['author']['group'],
                                                                  ticket['sent'].strftime("%d %b %Y: %H:%M")))
                                        for ticket in tickets]
        if request.method == 'POST' and form.validate_on_submit():
            Tickets.find_one_and_update({'_id': mongo_oid(form.data.get('selected_ticket'))},
                                        {'$set':
                                             {'checked': datetime.utcnow(),
                                              'answ_body': form.data.get('answ_body'),
                                              'public': form.data.get('make_public')}})
            flash('Ticket answer saved')
        for field, errors in form.errors.items():
            for message in errors:
                flash(message)
        return render_template('tutor/answer_ticket.html',
                               tickets=tickets,
                               form=form,
                               page=page,
                               pages=pages)
