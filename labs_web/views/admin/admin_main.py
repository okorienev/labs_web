from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort
from labs_web.extensions import admin, db, models
from . import AddGroup


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 3  # role 3 is admin role

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class UserView(AdminView):
    column_exclude_list = ['_password']
    column_list = ['name', 'username', 'email', 'active', 'role_obj']


class ReportView(AdminView):
    column_exclude_list = ['report_hash', 'report_stu_comment']


class RoleView(AdminView):
    column_list = ['role_id', 'role_name']
    can_create = False
    can_edit = False
    can_delete = False
    can_export = False


admin.add_view(UserView(models.User, db.session, endpoint='user_t'))  # this crutch solves problem when both app
admin.add_view(AdminView(models.Group, db.session))                   # blueprint 'user' and created by flask-admin
admin.add_view(ReportView(models.Report, db.session))                  # model blueprint have the same name
admin.add_view(AdminView(models.Course, db.session))                  # flask blueprints require to have unique names
admin.add_view(RoleView(models.Role, db.session))
admin.add_view(AddGroup(name='add_group', endpoint='add-group'))

