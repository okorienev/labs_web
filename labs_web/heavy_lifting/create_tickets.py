from labs_web.extensions import Tickets, Group
from random import choice, randint
from datetime import datetime
from copy import deepcopy
import warnings


def create_tickets():
    """
    fill MongoDB ticket collection
    """
    if Tickets.count() > 0:  # don't write to non-empty collection
        warnings.warn(Tickets.count())
        warnings.warn("wtf?")
        return
    for group in Group.query.all():
        for student in group.students:
            c = choice(group.courses)
            ticket_unaswered = {
                'author': {
                    'id': student.id,
                    'name': student.name,
                    'group': group.name
                },
                'course': {
                    'id': c.course_id,
                    'name': c.course_name
                },
                'topic': f"{student.name}-{c.course_shortened}",
                'body': f"{student.name} - {c.course_name}",
                'sent': datetime.utcnow()
            }
            ticket_answered = deepcopy(ticket_unaswered)
            ticket_answered.update({
                'checked': datetime.utcnow(),
                'answ_body': f"{c.course_tutor_obj.name} - {c.course_name}",
                'public': bool(randint(0, 1))
            })
            Tickets.insert_one(ticket_unaswered)
            Tickets.insert_one(ticket_answered)

