from flask import Flask, request
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sentry_sdk

# Set up sentry monitoring
sentry_sdk.init(
    dsn="https://glet_242be86fd52f0c7a1dddfafc15044010@observe.gitlab.com:443/errortracking/api/v1/projects/53835183",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=0.7,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# Create the Flask app
app = Flask(__name__, static_folder='./static', static_url_path='/')
db = SQLAlchemy()

# load configuration from config.cfg
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# New method for SQLAlchemy version 3 onwards
with app.app_context():
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    from .models import Entry, User, Image

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return db.session.get(User, int(user_id))
        
    db.create_all()
    db.session.commit()
    print('Created Database!')
    from . import routes