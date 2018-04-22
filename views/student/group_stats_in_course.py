from flask.views import View
from flask import request, redirect, render_template, abort
from flask_login import current_user
from functools import wraps


def user_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        return f(*args, **kwargs)
    return decorator


class GroupStats(View):
    @user_required
    def dispatch_request(self):
        return render_template('group_stats.html')

