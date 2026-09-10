from flask import render_template, session
from flask_wtf.csrf import Blueprint

from music.authentication.services import AuthService

# Create the blueprint
errors = Blueprint('errors', __name__)

root_blueprint = Blueprint('root', __name__)

@root_blueprint.route('/', methods=['GET'])
def homepage():

    return render_template(
        'homepage.html',
    )
