from flask import Flask
from config import Config
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api
from app import utils
from flask_cors import CORS

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api(doc='/docs')

def create_app(TestConfig=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # serve index page
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    CORS(app)

    if TestConfig:
        # load the test config if passed in
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app, default="api for Accommodation Web Portal",  
          title="Accommodation Web Portal", 
          description="api for Accommodation Web Portal")


    from app import accommodation, auth, reservation, review, search, user,recommendation#, favourite, 

    api.add_namespace(accommodation.api)
    api.add_namespace(auth.api)
    api.add_namespace(recommendation.api)
    api.add_namespace(reservation.api)
    api.add_namespace(review.api)
    api.add_namespace(search.api)
    api.add_namespace(user.api)
    #api.add_namespace(favourite.api)

    return app
