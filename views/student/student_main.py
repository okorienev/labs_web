# TODO stats for group in course
# TODO add check for report for lab already present in base
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from forms import ReportSendingForm
from models import *
from config import Config
from os.path import join
from hashlib import md5
from datetime import datetime, timezone
student = Blueprint('student',
                    __name__,
                    url_prefix='/student')


@student.route('/report/', methods=['GET', 'POST'])
@login_required
def give_report():
    form = ReportSendingForm()
    query = text("SELECT course_shortened, course_name, labs_amount "  # query gets courses of user with given id
                 "FROM "
                 "(SELECT course_id, user_id "
                 "FROM group_courses "
                 "JOIN user_groups "
                 "ON group_courses.group_id = user_groups.group_id) AS g "
                 "JOIN course ON g.course_id = course.course_id "
                 "WHERE user_id = :user_id"
                 )
    courses_of_user = [{'name': i.course_name, 'shortened': i.course_shortened}
                       for i in db.engine.execute(query, user_id=current_user.id)]

    if request.method == 'POST' and form.validate_on_submit():
        list_of_shortened = [i['shortened'] for i in courses_of_user]

        if request.form.get('course') not in list_of_shortened:  # user's group should have this course
            flash('You don\'t have this course')
            return redirect(request.url)

        query = text("""SELECT course.labs_amount FROM course WHERE course_shortened = :shortened""")
        lab_max_amount = [i['labs_amount'] for i in db.engine.execute(query, shortened=request.form.get('course'))][0]

        if int(request.form.get('number_in_course')) < 1 or \
           int(request.form.get('number_in_course')) > int(lab_max_amount):
            flash('lab number out of range')  # lab number should be in range between 1 and max lab number in course
            return redirect(request.url)
        # file uploading
        file = form.attachment.data
        if (lambda filename: '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf')(file.filename):
            filename = request.form.get('number_in_course') + '.pdf'  # filename is <number_in_course>.pdf
            query = text("""SELECT "group".name 
                            FROM user_groups
                            JOIN "group" ON user_groups.group_id = "group".group_id
                            WHERE user_id = :user_id""")
            group = [i.name for i in db.engine.execute(query, user_id=current_user.id)][0]
            # saving file to uploads
            file.save(join(Config.UPLOAD_PATH,
                           request.form.get('course'),
                           group,
                           current_user.name.split()[1],
                           filename))
            # generating md5 for report
            hash_md5 = md5()
            with open(join(Config.UPLOAD_PATH,
                           request.form.get('course'),
                           group,
                           current_user.name.split()[1],
                           filename), 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):  # read file by small chunks to avoid problems with memory
                    hash_md5.update(chunk)
            # creating new report
            report = Report(
                report_course=Course.query.filter_by(course_shortened=request.form.get('course')).first().course_id,
                report_student=current_user.id,
                report_num=request.form.get('number_in_course'),
                report_stu_comment=request.form.get('comment'),
                report_uploaded=datetime.now(timezone.utc),
                report_hash=hash_md5.hexdigest()
            )
            # adding report to database
            db.session.add(report)
            db.session.commit()
    return render_template('give_report.html', user=current_user, form=form, courses=courses_of_user)

