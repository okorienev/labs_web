from flask import Blueprint
from . import (ForgotPassword,
               RestorePassword)

user = Blueprint('user',
                 __name__,
                 url_prefix='/user')

user.add_url_rule('/forgot/', view_func=ForgotPassword.as_view('forgot-password'))
user.add_url_rule('/restore/<string:token>', view_func=RestorePassword.as_view('restore-password'))
