from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_migrate import Migrate # We can add this later if we need migrations

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
# migrate = Migrate() # For database migrations

def create_app(config_class_name="config.DevelopmentConfig"):
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Load configuration from config.py based on the name
    # config.py is now at the project root, so direct import.
    import config # Should resolve to root config.py

    if isinstance(config_class_name, str):
        app.config.from_object(config.config_by_name[config_class_name])
    else: # if already a config object
        app.config.from_object(config_class_name)


    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    # migrate.init_app(app, db) # For database migrations

    # Configure Flask-Login
    login_manager.login_view = 'auth.login' # The route for the login page (blueprint 'auth', route 'login')
    login_manager.login_message_category = 'info' # Flash message category

    # Register blueprints here
    from .auth import auth_bp # Import blueprint from auth package __init__
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .main import main_bp # Import blueprint from main package __init__
    app.register_blueprint(main_bp)

    # Example: Register admin, assessor, fse_owner blueprints if they are substantial
    # from .admin.routes import admin_bp
    # app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create database tables if they don't exist
    # This is okay for development, but for production, migrations (Flask-Migrate) are better.
    # Routes are now imported when their respective blueprint packages (auth, main) are imported.
    with app.app_context():
        from . import models # Import models here to avoid circular imports
        db.create_all()
        # You might want to add a function to seed initial data like ChecklistParts here
        seed_checklist_parts(db)


    @login_manager.user_loader
    def load_user(user_id):
        # Since the user ID is just the primary key of our user table,
        # use it in the query for the user
        from .models import User # Import here to avoid circularity
        return User.query.get(int(user_id))

    return app

def seed_checklist_parts(db_instance):
    from .models import ChecklistPart
    # Check if parts already exist to avoid duplicates if app restarts
    if ChecklistPart.query.count() == 0:
        parts_data = [
            {"part_name": "Part 2: Documentations", "max_score": 20, "description": "Hygiene Certificate of food handlers, Business Operating Permit, Suitability Permit, Hygiene Permit"},
            {"part_name": "Part 3: Personal Hygiene of Food handlers", "max_score": 20, "description": "Assessment of personal hygiene practices."},
            {"part_name": "Part 4: Material sourcing", "max_score": 20, "description": "Verification of material sources and quality."},
            {"part_name": "Part 5: Water Sources and Storage", "max_score": 10, "description": "Assessment of water sources and storage practices."},
            {"part_name": "Part 6: Waste Disposal", "max_score": 20, "description": "Evaluation of waste disposal methods and compliance."},
            {"part_name": "Part 7: Cleaning", "max_score": 10, "description": "Assessment of cleaning procedures and schedules."}
        ]
        for part_data in parts_data:
            part = ChecklistPart(**part_data)
            db_instance.session.add(part)
        db_instance.session.commit()
        print("Checklist parts seeded.")
    else:
        print("Checklist parts already exist.")
