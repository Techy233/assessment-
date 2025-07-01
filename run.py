import os
# Adjust imports to reflect new location of run.py and fse_portal package
from fse_portal.app import create_app, db
from fse_portal.app.models import User, FSE, Assessment, ChecklistPart, AssessmentScore
# from flask_migrate import Migrate # If using migrations

# Determine config name (e.g., 'dev', 'prod') from environment variable or default to 'dev'
# The create_app factory now expects the actual config object or its name string.
# config.py is now at the root, so create_app can import it directly.
# The FLASK_CONFIG env var can still be used to select the config name.
env_config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(env_config_name) # Pass the name, create_app will use config_by_name

# If using Flask-Migrate
# migrate = Migrate(app, db)

# You can define a shell context processor to make certain objects available in `flask shell`
@app.shell_context_processor
def make_shell_context():
    # Models are already imported above
    return {'db': db, 'User': User, 'FSE': FSE, 'Assessment': Assessment,
            'ChecklistPart': ChecklistPart, 'AssessmentScore': AssessmentScore}

if __name__ == '__main__':
    # The host='0.0.0.0' makes the server accessible externally if needed (e.g. in a Docker container)
    # Debug should ideally be loaded from config
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', True))
