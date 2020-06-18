from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import CourseSnapshotForm, celery, Course, redis_conn, db, minio
from labs_web import app
from flask import render_template, request, flash
from datetime import datetime

from labs_web.extensions.models import File
from .MarksWriter import MarksWriterFactoryMethod
from labs_web.views.student.group_stats_in_course import ReportsProcessor
from secrets import token_hex
import shutil
import os
import os.path as p
import logging


log = logging.getLogger(__name__)


@celery.task(ignore_result=True)
def make_course_snapshot(course_id: int, marks_format: str):
    with app.app_context():
        time = datetime.utcnow()
        course = Course.query.get(course_id)
        path_to_snapshot = p.join(app.config['UPLOAD_PATH'], 'snapshots',
                                  'Snapshot_{}_{}'.format(course.course_shortened,
                                                          time.strftime('%d-%m-%Y %H:%M')))
        shutil.copytree(p.join(app.config['UPLOAD_PATH'], course.course_shortened),
                        path_to_snapshot)  # copy uploads to temp directory
        for group in course.groups:
            for student in group.students:
                try:
                    os.rename(p.join(path_to_snapshot, group.name, str(student.id)),  # rename folders with students'
                              p.join(path_to_snapshot, group.name, str(student.name)))  # reports for being
                except FileNotFoundError:  # human-readable
                    os.makedirs(p.join(path_to_snapshot, group.name, str(student.name)), exist_ok=True)
                    # print('{} has no uploaded reports in course {}'.format(student.name,
                    #                                                        course.course_shortened))
        writer = MarksWriterFactoryMethod.writer(marks_format)
        for group in course.groups:
            reports_raw = ReportsProcessor.generate_marks(group, course_id)  # saving marks table
            reports = [{'name': i.name,
                        'marks': i.reports} for i in reports_raw]
            writer.write(reports, p.join(path_to_snapshot, group.name, "{}-Marks.{}".format(group.name,
                                                                                            marks_format)))
        prev_path = os.getcwd()
        os.chdir(p.join(app.config['UPLOAD_PATH'], 'snapshots'))

        name = 'Snapshot-{}-{}'.format(course.course_shortened, time.strftime('%d-%m-%Y %H:%M'))
        shutil.make_archive(name, format='zip', root_dir=path_to_snapshot)
        bucket = app.config['MINIO']['buckets']['snapshots']
        # adding file record to db
        key = token_hex(32)
        archive_path = f'{name}.zip'
        file = File(
            owner_id=course.course_tutor,
            file_name=archive_path,
            bucket=bucket,
            file_type=File.Type.snapshot,
            key=key
        )
        db.session.add(file)
        db.session.commit()
        stat = os.stat(archive_path)
        with open(archive_path, 'rb') as f:
            minio.client.put_object(bucket, key, f, stat.st_size)
        os.remove(archive_path)
        os.chdir(prev_path)
        shutil.rmtree(path_to_snapshot)
        redis_conn.set('snapshot-timeout-{}'.format(course.course_tutor), value='some', ex=1 * 60)


class CourseSnapshot(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        timeout = redis_conn.exists('snapshot-timeout-{}'.format(current_user.id))
        form = CourseSnapshotForm()
        form.course.choices = [(course.course_id, course.course_name) for course in current_user.courses]
        snapshots = (
            db.session.query(File)
            .filter(
                File.owner_id == current_user.id,
                File.file_type == File.Type.snapshot,
            )
            .order_by(File.file_id.desc())
            .all()
        )
        if request.method == "POST" and form.validate_on_submit():
            make_course_snapshot.delay(form.data.get('course'), form.data.get('marks_format'))
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)
        return render_template('tutor/course_snapshot.html',
                               form=form,
                               timeout=timeout,
                               snapshots=snapshots)
