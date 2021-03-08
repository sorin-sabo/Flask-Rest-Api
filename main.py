#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os

import flask_monitoringdashboard as dashboard
from flask import Flask, Blueprint
from flask import jsonify
from marshmallow.exceptions import ValidationError

from api.app import api
import api.utils.responses as resp
from api.config import DevelopmentConfig, ProductionConfig
from api.routes import author_ns
from api.utils import AuthError, response_with, db

app = Flask(__name__)
dashboard.bind(app)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(author_ns)

app.register_blueprint(blueprint)


@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


@app.errorhandler(AuthError)
def handle_auth_error(e):
    logging.error(e)
    response = jsonify(e.error)
    response.status_code = e.status_code
    return response


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    logging.error(e)
    response = jsonify(dict(code='validation_error', message=e.messages))
    response.status_code = 400
    return response


db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
