from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from os import path
#helps us deal with finding a user once we have logged in
from flask_login import LoginManager

#db = database
#start by defining a new database. this is database used when something is added/new user is created
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    #encrpyts and secures session data related to website 
    app.config['SECRET_KEY'] = 'should besecretinproduction'
    #tell flask we are using database and where the database will be located
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'# where db is stored//f allows us to use {} in python code
    #initialise db by giving it our flask app
    db.init_app(app)

    #imorting blueprints
    from .views import views
    from .auth import auth

    #register blueprints, prefix what needs to be entered to access e.g /auth in url
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #creating db, checks before server is run is db created yet?
    from .models import User, Note

    create_database(app)

    #finding a user once we login
    login_manager = LoginManager()
    #if there is a login required where should flask redirect user to
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # confirming with flask the user that we are looking for

    return app

# check if db exists and if not, create it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)# pass app tells sqlalchemy which app we are creating the db for
        print('Created Database!')