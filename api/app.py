from flask_restx import Api
from api.config import settings

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'implicit',
        'tokenUrl': f'{settings.OAUTH_DOMAIN}/token',
        'authorizationUrl': f'{settings.OAUTH_DOMAIN}/authorize?audience={settings.AUTH0_ACCESS_AUDIENCE}',
        'scopes': {
            'openid': 'Get ID token',
            'profile': 'Get identity',
        }
    }
}

api = Api(
    version='1.0',
    title='Flask REST API',
    description='Flask REST API',
    contact='Sorin Sabo',
    contact_email='sabo.sorin@ymail.com',
    doc='/docs',
    security=[{'oauth2': 'openid'}],
    authorizations=authorizations
)
