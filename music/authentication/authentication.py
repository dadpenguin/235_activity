from functools import wraps

from flask import Blueprint, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from .services import AuthService, AuthenticationException, NameNotUniqueException, UnknownUserException
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo

authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication'
)

class CredentialFieldsMissing(Exception):
    pass


class RepoFailedToInitialize(Exception):
    pass

@authentication_blueprint.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None


    if repo.repo_instance is None:
        raise RepoFailedToInitialize()

    if form.validate_on_submit():
        username = form.user_name.data
        password = form.password.data

        if username is None or password is None:
            raise CredentialFieldsMissing("username or password is missing")
        try:
            AuthService.add_user(username, password, repo.repo_instance)

            return redirect(url_for('authentication_bp.login'))

        except NameNotUniqueException:
            user_name_not_unique = 'Your user name is already taken - Please supply another'

    # TODO: create the template

    return render_template(
            'authentication/credentials.html',
            title='Register',
            form=form,
            user_name_error_message=user_name_not_unique,
            handler_url=url_for('authentication_bp.register')
        )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None


    if repo.repo_instance is None:
        raise RepoFailedToInitialize()


    if form.validate_on_submit():
        username = form.user_name.data
        password = form.password.data

        if username is None or password is None:
            raise CredentialFieldsMissing("username or password is missing")
        try:
            AuthService.authenticate_user(username,password, repo.repo_instance)

            session.clear()

            session['user_name'] = form.user_name.data
            return redirect(url_for('root.homepage'))

        except UnknownUserException:
            user_name_not_recognised = 'user name not recognized, please supply another'

        except AuthenticationException:
            password_does_not_match_user_name = 'Password does not match the supplied user name - Please check and try again'

    # TODO: complete the template blueprint
    return render_template(
           'authentication/credentials.html',
           title='Login',
           user_name_error_message=user_name_not_recognised,
           password_error_message=password_does_not_match_user_name,
           form=form,
       )





# TODO: create authentication blueprint
@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('root.homepage'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


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
    user_name = StringField("User_name", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])

    submit = SubmitField('Login')
