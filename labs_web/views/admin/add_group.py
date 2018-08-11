from flask_admin import BaseView, expose
from flask_login import current_user
from flask import request, render_template
from labs_web.extensions import Group, User, celery, mail, db
from flask_mail import Message
from labs_web import app
from random import choice
from string import ascii_letters, digits
import csv


@celery.task(ignore_result=True)
def notify_on_registration(email: str, **kwargs):
    """
    celery task to notify new user on registration and provide him/her login credentials
!it's unsafe to send login and password directly but service doesn't provide options for users to register themselves
all registration is done by service admin because whole group is registered at once not by one student 
    :param email: user email 
    :param kwargs: name, group, username & password to format mail template
    :return: None
    """
    with app.app_context():
        msg = Message()
        msg.recipients = [email]
        msg.sender = ['labs.web.notifications']
        msg.subject = 'account registered'
        msg.html = render_template('mail/user_registered.html', **kwargs)
        print(msg.html)
        mail.send(msg)


class AddGroup(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 3

    @expose('/', methods=["GET", "POST"])
    def add_group(self):
        if request.method == "POST":
            group = Group(name=request.form.get('group'))
            db.session.add(group)
            reader = csv.reader([i.decode() for i in request.files.get('file').read().splitlines()][1::])
            counter = 1
            for row in reader:
                assert len(row) == 2
                student = User(name=row[0], email=row[1], role=1)
                student.username = "{}_stu_{}".format(group, counter)
                counter += 1
                password = ''.join(choice(ascii_letters + digits) for i in range(15))
                student.set_password(password)
                db.session.add(student)
                group.students.append(student)
                notify_on_registration.delay(email=student.email,
                                             name=student.name,
                                             group=group.name,
                                             username=student.username,
                                             password=password)
                db.session.commit()
        return self.render('admin/add_group.html')
