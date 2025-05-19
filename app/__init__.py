from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'superdupersecret'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'

    #  Get absolute base path
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Ensure instance folder exists
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)

    # Build full path to the DB file
    db_path = os.path.join(instance_path, 'users.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    db.init_app(app)
    csrf.init_app(app)

    
    from app.routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)


    with app.app_context():
        from app import models 
        db.create_all()

        
    return app