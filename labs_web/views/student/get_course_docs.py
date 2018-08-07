from flask.views import View
from flask_login import login_required, current_user
from flask import send_file, redirect, url_for, current_app, flash
from labs_web.extensions import Course
import os.path as p
import os


class GetCourseDocs(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        course = Course.query.get(kwargs.get('course_id'))
        if not course or course.course_id not in [i.course_id for i in current_user.group[0].courses]:
            return redirect(url_for('student.student_home'))
        docs_directory = p.join(current_app.config.get('UPLOAD_PATH'), current_app.config.get("DOCS_FOLDER"))
        if p.exists(docs_directory) and p.isdir(docs_directory):
            try:
                doc_archive = [i for i in filter(lambda filename: course.course_shortened in filename,
                                                 os.listdir(docs_directory))][0]
                return send_file(p.join(docs_directory, doc_archive))
            except IndexError:
                flash('Docs not found. Please contact course tutor and/or web service administration')
                return redirect(url_for('student.student_home'))
        else:
            flash('Some internal error occurred, please contact the administrator and report your actions')
            return redirect(url_for('student.student_home'))
