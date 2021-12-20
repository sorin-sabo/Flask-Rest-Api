"""
OAuth module definition
"""

import base64
import json
from functools import wraps

import jwt
import requests
import six
# noinspection PyProtectedMember
from flask import request, _request_ctx_stack
from jwt.algorithms import RSAAlgorithm

from apps.api.models import User
from config import settings
from .exceptions import AuthError


def get_token_auth_header():
    """
    Obtains the access token from the Authorization Header

    :return:
        - Request's 'Authorization' Id/Access token - When correct Authorization:' header
    :raise:
        - AuthError: 401:
            - In case token type is invalid.
            - In case token split by space length is != 2
    """
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'message': 'Invalid Authorization header. Authorization header is missing.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Invalid Authorization header. Token type must be Bearer.'
        }, 401)

    if len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Invalid Authorization header. No credentials provided.'
        }, 401)

    if len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Invalid Authorization header. Credentials string should not contain spaces.'
        }, 401)

    token = parts[1]

    return token


def verify_jwt_token():
    """
    Verify JWT Token
    """

    token = get_token_auth_header()
    rsa_key = _get_rsa_key(token)

    if not rsa_key:
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Unable to find appropriate key'
        }, 401)

    token_type, payload = _get_token_type(token)

    # Guest doesn't have audience under 'aud' but under 'client_id'
    audience = settings.OAUTH2_CLIENT if token_type == 'id' else None

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=audience,
            issuer=f'{settings.OAUTH2_DOMAIN}'
        )
    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'message': 'token is expired'
        }, 401)
    except (jwt.InvalidTokenError, jwt.DecodeError) as exc:
        raise AuthError({
            'code': 'invalid_header',
            'message': f'Unable to parse authentication token. {str(exc)}'
        }, 401)

    # Post validate audience for guest
    if token_type == 'access':
        validate_access_token_claims(payload)

    if token_type == 'id':
        user = get_token_user(payload)
        _request_ctx_stack.top.user = user


def requires_auth(func):
    """
    Determines if the access token is valid
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        """
        JWT Token verification
        """
        verify_jwt_token()

        return func(*args, **kwargs)

    return decorated


def validate_access_token_claims(token_decoded):
    """
    Access token validation
    """
    if settings.OAUTH2_GUEST is None and 'client_id' not in token_decoded:
        # Application did not specify an audience, but
        # the token has the 'aud' claim
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Invalid audience'
        }, 401)

    audience_claims = token_decoded['client_id']

    if isinstance(audience_claims, six.string_types):
        audience_claims = [audience_claims]

    if settings.OAUTH2_GUEST not in audience_claims:
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Invalid audience'
        }, 401)


def _get_rsa_key(token):
    """
    Get rsa key(public key) from token
    Details https://jwt.io/

    :param str token: Id/Access token
    :return: token public key after validation with RSAAlgorithm
    """

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.DecodeError as exc:
        raise AuthError({
            'code': 'invalid_header',
            'message': f'Invalid header. {str(exc)}'
        }, 401)
    if unverified_header['alg'] == 'HS256':
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Invalid header. Use an RS256 signed JWT Access Token'
        }, 401)

    jwk_keys = _json_web_keys()
    jwk_data = jwk_keys.get(unverified_header['kid'])

    if jwk_data:
        return RSAAlgorithm.from_jwk(jwk_data)

    return None


def _json_web_keys():
    """
    Get web keys from auth domain

    :return: Domain keys. Result can be cached based on requirements since is always the same.
    :rtype dict
    """
    response = requests.get(f'{settings.OAUTH2_DOMAIN}/.well-known/jwks.json')
    response.raise_for_status()
    json_data = response.json()

    return {item['kid']: json.dumps(item) for item in json_data['keys']}


def _get_token_type(token):
    """
    Establish token type is ID Token or Access Token.

    :return 'id' or 'access' - based on token_use received from AWS;
            token payload - token payload data decoded using base64 library;
    :rtype str, dict
    """
    token_payload_data = _decode_token_using_base64(token)

    return token_payload_data.get('token_use', 'id'), token_payload_data


def _decode_token_using_base64(token):
    """
    Decode token using base64 library
    :return Token decoded payload data in case decode process completes successfully
            Emtpy dictionary otherwise
    :rtype dict
    """

    if isinstance(token, six.text_type):
        token = token.encode('utf-8')

    # Decode token using base64
    try:
        signing_value, _ = token.rsplit(b'.', 1)
        _, claims_segment = signing_value.split(b'.', 1)

        rem = len(claims_segment) % 4

        if rem > 0:
            claims_segment += b'=' * (4 - rem)

        decoded_token = base64.urlsafe_b64decode(claims_segment)
        decoded_token = json.loads(decoded_token)

    except (ValueError, TypeError, AttributeError):
        decoded_token = {}

    return decoded_token


def get_token_user(token_user):
    """
    User token retrieve
    """
    if token_user.get('email') is None:
        raise AuthError({
            'code': 'unauthorized_user',
            'message': 'Invalid request user. Please contact system '
                       'administrator for more information.'
        }, 401)

    if not token_user.get('email_verified', False):
        raise AuthError({
            'code': 'unauthorized_user',
            'message': 'Invalid request user. Please verify your email address and try again.'
        }, 401)

    user = User.query.filter_by(email=token_user.get('email')).first()

    if user is None:
        raise AuthError({
            'code': 'unauthorized_user',
            'message': 'Invalid request user. Please contact system '
                       'administrator for more information.'
        }, 401)

    return user
