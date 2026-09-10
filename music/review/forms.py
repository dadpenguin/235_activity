from flask_wtf.form import FlaskForm
from wtforms import IntegerField
from wtforms.fields.simple import HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class ReviewForm(FlaskForm):
    track_id = HiddenField("Track ID", validators=[DataRequired()])
    paragraph = TextAreaField("Review", validators=[DataRequired()])
    stars = IntegerField(
        "Rating (1-5)",
        validators=[
            DataRequired(),
            NumberRange(
                min=1, max=5, message="Stars must be between 1 and 5."
            ),
        ],
    )
    submit = SubmitField('Submit Review')
