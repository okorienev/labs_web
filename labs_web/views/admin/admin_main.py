from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort
from labs_web.extensions import admin, db, models


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 3  # role 3 is admin role

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class UserView(AdminView):
    column_exclude_list = ['_password']


class ReportView(AdminView):
    column_exclude_list = ['report_hash', 'report_stu_comment']

admin.add_view(UserView(models.User, db.session, endpoint='user_t'))  # this crutch solves problem when both app
admin.add_view(AdminView(models.Group, db.session))                   # blueprint 'user' and created by flask-admin
admin.add_view(ReportView(models.Report, db.session))                  # model blueprint have the same name
admin.add_view(AdminView(models.Course, db.session))                  # flask blueprints require to have unique names

