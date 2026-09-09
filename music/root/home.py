from flask import render_template, session
from flask_wtf.csrf import Blueprint

from music.authentication.services import AuthService


root_blueprint = Blueprint('root', __name__)

@root_blueprint.route('/', methods=['GET'])
def homepage():

    return render_template(
        'homepage.html',
    )
