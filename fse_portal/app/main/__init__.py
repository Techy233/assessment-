from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='templates')

# Import routes after blueprint creation to define the routes on the blueprint
from . import routes
