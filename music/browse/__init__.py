from flask import Blueprint

browse_blueprint = Blueprint('browse_bp', __name__)
from music.browse import browse