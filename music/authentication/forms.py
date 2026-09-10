from flask_wtf.csrf import ValidationError
from flask_wtf.form import FlaskForm
from password_validator.password_validator import PasswordValidator
from wtforms.fields.simple import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = (
                "Your password must be at least 8 characters, and contains an upper case letter,\
            a lower case and a digit"
            )

        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()

        schema.min(8).has().uppercase().has().lowercase().has().digits()

        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField(
        "Username",
        [
            DataRequired(message="Your user name is required"),
            Length(min=3, message="your username is too short"),
        ],
    )

    password = PasswordField(
        "Password", [DataRequired(message="Your password is required"), PasswordValid()]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    user_name = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])

    submit = SubmitField('Login')
