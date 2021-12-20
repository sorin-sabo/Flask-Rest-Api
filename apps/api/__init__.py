"""
Flask app initialization
"""

from flask import Blueprint
from flask_restx import Api

from apps.api.controllers import author_ns, book_ns
from config import settings

blueprint = Blueprint('api', __name__, url_prefix='/api')

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'implicit',
        'tokenUrl': f'{settings.OAUTH2_DOMAIN}/token',
        'authorizationUrl': f'{settings.OAUTH2_DOMAIN}/authorize?audience={settings.OAUTH2_GUEST}',
        'scopes': {
            'openid': 'Get ID token',
            'profile': 'Get identity',
        }
    }
}

api = Api(
    blueprint,
    version='1.0',
    title='Flask REST API',
    description='Flask REST API',
    contact='Sorin Sabo',
    contact_email='sabo.sorin@ymail.com',
    doc='/docs',
    security=[{'oauth2': 'openid'}],
    authorizations=authorizations,
)

api.add_namespace(author_ns)
api.add_namespace(book_ns)
