from flask.views import View
from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from models import Course
from forms import CourseChoosingForm


class ChooseCourseToCheck(View):
    """View to choose course to check reports in"""
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        courses = [{'shortened': course.course_shortened,
                    'name': course.course_name} for course in
                   Course.query.filter_by(course_tutor=current_user.id).all()]  # list of courses for tutor
        form = CourseChoosingForm()
        if request.method == "POST" and form.validate_on_submit():
            if form.data.get('shortened') not in [i['shortened'] for i in courses]:  # if course isn't present for tutor
                flash('You don\' have this course')
                return redirect(request.url)

            chosen_course = Course.query.filter_by(course_tutor=current_user.id,
                                                   course_shortened=form.data.get('shortened')).first()
            return redirect(url_for('tutor_check_reports'),
                            {'course_id': chosen_course.id})
        return render_template('tutor_choose_course.html', courses=courses, form=form)







