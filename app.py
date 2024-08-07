from flask import Flask
from flask_migrate import Migrate
from create_initial_data import create_data
from application.database import *
from application.sec import user_datastore
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore, Security
import resources
import application.controllers

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lmsdata.sqlite3"
    app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-salt'

    # configure token
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['SECURITY_TOKEN_MAX_AGE'] = 3600 #1hr
    app.config['SECURITY_LOGIN_WITHOUT_CONFIRMATION'] = True
    
    db.init_app(app)
    app.migrate=Migrate(app, db)
    app.security = Security(app, user_datastore)
        
    with app.app_context():
        
        db.create_all()
        create_data(user_datastore)

    application.controllers.create_views(app, user_datastore)  
    
    #connect flask to flask restful
    resources.api.init_app(app)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run()

