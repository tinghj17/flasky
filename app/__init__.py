from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# load_dotenv is a function
from dotenv import load_dotenv
import os

# create the object
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

from .models.cars import Car
# from .routes.cars import cars_bp
from .models.drivers import Driver

# flask needs to find this function
def create_app(testing = None):
    # __name__ stores the name of the module we're in
    # creating a new flask object
    app = Flask(__name__)

    # put configuration, for legacy.
    app.config["SQLALCHEMY_TEACK_MODIFICATIONS"] = False
    if testing is None:
        # tell sqlalchemy where is our database by using connection string 
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        app.config["TESTING"] =  True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('TESTING_SQLALCHEMY_DATABASE_URI')
    
    # initialize the application, hooking up the application 
    # connect db object to flask server
    db.init_app(app)
    migrate.init_app(app,db)
    # to get the blueprint
    from .routes.cars import cars_bp
    from .routes.drivers import drivers_bp

    # tell the flask about the blueprint
    app.register_blueprint(cars_bp)
    app.register_blueprint(drivers_bp)

    return app