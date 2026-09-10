from functools import wraps

from flask import Blueprint, redirect, render_template, request, session, url_for
from flask.helpers import abort
from password_validator import PasswordValidator
from wtforms.validators import ValidationError

import music.adapters.repository as repo
from music.authentication.exceptions import (
    CredentialFieldsMissing,
    RepoFailedToInitialize,
)
from music.authentication.forms import LoginForm, RegistrationForm

from .services import (
    AuthenticationException,
    AuthService,
    NameNotUniqueException,
    UnknownUserException,
)

authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication'
)



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

    return render_template(
           'authentication/credentials.html',
           title='Login',
           user_name_error_message=user_name_not_recognised,
           password_error_message=password_does_not_match_user_name,
           form=form,
       )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('root.homepage'))

def login_required(view_func):
    """Decorator to enforce authentication for route handlers."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        user_name = AuthService.get_authenticated_user_name()
        if not user_name:
            if request.method == "GET":
                return redirect(url_for('authentication_bp.login'))
            abort(401)
        return view_func(user_name, *args, **kwargs)
    return wrapped_view
