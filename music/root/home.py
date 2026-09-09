from flask import render_template
from flask_wtf.csrf import Blueprint

root_blueprint = Blueprint('root', __name__)

@root_blueprint.route('/', methods=['GET'])
def homepage():

    return render_template(
        'homepage.html',
    )
