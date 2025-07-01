from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Import routes after blueprint creation to define the routes on the blueprint
from . import routes
