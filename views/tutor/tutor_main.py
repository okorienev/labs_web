from flask import Blueprint, render_template
from flask_login import login_required
from views.tutor.tutor_choose_course_to_check import ChooseCourseToCheck
from views.tutor.check_reports import CheckReports
tutor = Blueprint('tutor',
                  __name__,
                  url_prefix='/tutor')
tutor.add_url_rule('/choose-course/', view_func=ChooseCourseToCheck.as_view('tutor_choose_course'))
tutor.add_url_rule('check-<int:course_id>', view_func=CheckReports.as_view('tutor_check_reports'))


@tutor.route('/home/')
@login_required
def tutor_home():
    return render_template('tutor_home.html')
