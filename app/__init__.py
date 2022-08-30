from flask import Flask
from .extensions import bcrypt, csrf, toastr
from .context_processor import common_context


def create_app():

    app = Flask(__name__)

    app.config.from_object('config.Config')

    app.context_processor(common_context)

    csrf.init_app(app)
    bcrypt.init_app(app)
    toastr.init_app(app)

    from .auth import auth
    from .user import user
    from .jobs import jobs
    from .contact import contact

    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(user, url_prefix = '/user')
    app.register_blueprint(jobs, url_prefix = '/job')
    app.register_blueprint(contact, url_prefix = '/contact')

    return app