from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_database():
    db.create_all()
    print('Database Created')

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'HGhkfhnb HKGhhHVHVBFAKhvbdfn fdvnsdbdfsk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nududu.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    # Import Blueprints
    from .views import views
    from .admin import admin
    from .auth import auth
    from .models import Customer, Product, Employee, Order, Cart

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
       create_database()

    return app
