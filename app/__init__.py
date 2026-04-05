from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app.storage import init_mongo

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '../static'))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secure-digital-governance-2024-secret-key'
    
    db.init_app(app)
    init_mongo(app)
    
    from app.routes import auth_routes, dashboard_routes, admin_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    app.register_blueprint(admin_routes.bp)
    
    with app.app_context():
        db.create_all()
    
    return app
