from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from redis import Redis
from app.utils import verify_env
import os


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address, default_limits=[])


def create_app(testing=False):
    load_dotenv()
    verify_env.check_env_variables_exist()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["RATELIMIT_ENABLED"] = False
        limiter.enabled = False

    # Attempt Redis connection within app context
    try:
        redis_client = Redis(host="localhost", port=6379)
        redis_client.ping()
    except Exception as e:
        raise RuntimeError(f"Redis connection failed: {e}")

    limiter.storage_uri = "redis://localhost:6379"
    limiter.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.main import main
    from app.routes.files import files

    app.register_blueprint(dashboard, url_prefix="/dashboard")
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(files, url_prefix="/files")

    with app.app_context():
        from app.models.user import User
        from app.models.uploaded_file import UploadedFile

        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User

        return User.query.filter_by(id=user_id).first()

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app
