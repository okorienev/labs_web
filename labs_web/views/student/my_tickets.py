from flask.views import View
from flask import render_template
from flask_login import login_required, current_user
from labs_web.extensions import Tickets


class MyTickets(View):
    decorators = [login_required]

    def dispatch_request(self):
        my_tickets = [ticket for ticket in Tickets.find({'author.id': current_user.id}).sort('sent', -1)]
        pending = filter(lambda ticket: not ticket.get('answ_body'), my_tickets)
        answered = filter(lambda ticket: ticket.get('answ_body') is not None, my_tickets)
        public = [ticket for ticket in Tickets.find(
            {'public': True,
             'course.id': {'$in': [i.course_id for i in current_user.group[0].courses]}}).sort('sent', -1)]
        return render_template('student/my_tickets.html',
                               pending=pending,
                               answered=answered,
                               public=public)
