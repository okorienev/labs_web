from flask.views import View
from flask import render_template
from flask_login import login_required, current_user
from labs_web.extensions import Tickets


class MyTickets(View):
    decorators = [login_required]

    def dispatch_request(self):
        my_tickets = [ticket for ticket in Tickets.find({'author.id': current_user.id}).sort('sent', -1)]
        return render_template('student/my_tickets.html',
                               pending=my_tickets,
                               answered=my_tickets,
                               public=my_tickets)
