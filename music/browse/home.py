from flask import render_template


from music.browse import root_blueprint

@root_blueprint.route('/', methods=['GET'])
def home():

    return render_template(
        'homepage.html',
    )
