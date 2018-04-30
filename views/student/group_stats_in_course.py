from flask.views import View
from flask import render_template


class GroupStats(View):
    def dispatch_request(self, *args, **kwargs):
        return render_template('group_stats.html')

