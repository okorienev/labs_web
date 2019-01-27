from flask.views import View
from flask_login import login_required, current_user
from flask import render_template, request, flash, current_app
import os.path as p
import os
import logging
from labs_web.extensions import AddCourseForm, Group, Course, db


class AddCourse(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = AddCourseForm()
        form.groups.choices = [(group.group_id, group.name) for group in Group.query.all()]
        if request.method == "POST" and form.validate_on_submit():
            new_course = Course(course_name=form.data.get('course_name'),
                                course_shortened=form.data.get('course_shortened'),
                                labs_amount=form.data.get('labs_amount'),
                                lab_max_score=form.data.get('lab_max_score'),
                                course_tutor=current_user.id)
            db.session.add(new_course)
            db.session.commit()
            course = Course.query.filter_by(course_shortened=form.data.get('course_shortened')).first()
            course.course_shortened = "{}#{}".format(course.course_shortened, course.course_id)
            course.groups.extend(Group.query.filter(Group.group_id.in_(form.data.get('groups'))).all())
            file = form.attachment.data
            path = p.join(current_app.config.get("UPLOAD_PATH"),
                          current_app.config.get("DOCS_FOLDER"),
                          course.course_shortened + '.zip')
            try:
                file.save(path)
            except FileNotFoundError:
                os.makedirs(p.join(current_app.config.get("UPLOAD_PATH"),
                                   current_app.config.get("DOCS_FOLDER")))
                file.save(path)
            flash("created course {} successfully".format(course.course_shortened))
            try:   # create folder for reports
                os.mkdir(p.join(current_app.config.get("UPLOAD_PATH"),
                                course.course_shortened))
            except FileExistsError:   # idk what's the case that file already exists but this is better than showing 500
                logging.warning(f"Directory for {course.course_name}({course.course_id}) already exists")
            db.session.commit()
        for field, messages in form.errors.items():
            for message in messages:
                flash(message)
        return render_template('tutor/add_course.html',
                               form=form)
