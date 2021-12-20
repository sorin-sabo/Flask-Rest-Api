import os
import pytest
import logging

from flask import jsonify
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from marshmallow.exceptions import ValidationError

from apps.api import blueprint
from apps.api.utils import response_with, responses as resp, AuthError, NotFound
from apps import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'default'))
app.register_blueprint(blueprint)

migrate = Migrate(app, db)
cli = FlaskGroup(app)


@cli.command('test')
def test():
    """Runs the unit tests."""
    pytest.main(args=['-v', 'tests'])


@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    db.session.rollback()
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    logging.error(e)
    response = jsonify(dict(code='validation_error', message=e.messages))
    response.status_code = 400
    return response


@app.errorhandler(NotFound)
def handle_not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


if __name__ == '__main__':
    cli()
