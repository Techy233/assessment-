import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_hard_to_guess_secret_string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other general configurations here

class DevelopmentConfig(Config):
    DEBUG = True
    # basedir is project root. We want db in fse_portal/app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'fse_portal', 'app.db')

class TestingConfig(Config):
    TESTING = True
    # basedir is project root. We want test_db in fse_portal/test_app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'fse_portal', 'test_app.db')
    WTF_CSRF_ENABLED = False # Disable CSRF for easier testing of forms

class ProductionConfig(Config):
    # Production specific configs
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # From environment variable
    # Ensure SECRET_KEY is set from environment in production
    if not Config.SECRET_KEY and os.environ.get('SECRET_KEY'):
        Config.SECRET_KEY = os.environ.get('SECRET_KEY')
    elif not Config.SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production application")

# Dictionary to access configs by name
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    default=DevelopmentConfig
)
