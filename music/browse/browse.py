import math

from flask import render_template, request

import music.adapters.repository as repo
import music.browse.services as services

from music.browse import browse_blueprint



def getTotalTracks():
    pass




@browse_blueprint.route('/', methods=['GET'])
def home():
    """
    display the homepage with an alphabetical list of tracks.
    """



    return render_template(
        'homepage.html',
    )
