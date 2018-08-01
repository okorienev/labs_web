from labs_web import app
from labs_web.views import (student,
                            tutor,
                            auth,
                            user)

app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(student)
app.register_blueprint(tutor)


if __name__ == '__main__':  # registers blueprints and runs server
    app.run(debug=True, host='0.0.0.0')
