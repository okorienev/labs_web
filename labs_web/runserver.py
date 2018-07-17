from labs_web import app
from labs_web.views import (student,
                            tutor,
                            auth,
                            admin,
                            user)


if __name__ == '__main__':  # registers blueprints and runs server
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(student)
    app.register_blueprint(tutor)
    app.register_blueprint(admin)
    app.run(debug=True)
