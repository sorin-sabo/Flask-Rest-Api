#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os

import flask_monitoringdashboard as dashboard
from flask import Flask
from flask import jsonify
from flask import send_from_directory
from flask_jwt_extended import JWTManager
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow.exceptions import ValidationError

import api.utils.responses as resp
from api.config import DevelopmentConfig, ProductionConfig
from api.routes import author_routes
from api.utils import AuthError, response_with, db

SWAGGER_URL = '/api/docs'

app = Flask(__name__)
dashboard.bind(app)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(author_routes, url_prefix='/api/authors')


@app.route('/avatar/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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


# END GLOBAL HTTP CONFIGURATIONS

@app.route("/api/spec")
def spec():
    swag = swagger(app, prefix='/api')
    swag['info']['base'] = "http://localhost:5000"
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Flask Rest Api"
    return jsonify(swag)


swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, '/api', config={'app_name': "Flask Sample App"})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
jwt = JWTManager(app)
db.init_app(app)

with app.app_context():
    # from api.models import *
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
