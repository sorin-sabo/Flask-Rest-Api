from flask import make_response, jsonify

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

SERVER_ERROR_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Not found"
}

FORBIDDEN_403 = {
    "http_code": 403,
    "code": "notAuthorized",
    "message": "You are not authorised to execute this."
}
UNAUTHORIZED_401 = {
    "http_code": 401,
    "code": "notAuthorized",
    "message": "Invalid authentication."
}

NOT_FOUND_HANDLER_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "route not found"
}

SUCCESS_200 = {
    'http_code': 200,
    'code': 'success'
}

SUCCESS_201 = {
    'http_code': 201,
    'code': 'success'
}

SUCCESS_204 = {
    'http_code': 204,
    'code': 'success'
}


def response_with(response, value=None, error=None, headers=None, pagination=None):
    """
    Make response from Flask library to create standard responses for APIs.

    :param dict response: Represent by one of above response types
    :param value: Value to return as response
    :param error: Error to return in response body
    :param headers: Response headers. Added mainly to avoid CORS issues.
    :param pagination: Response pagination in case of filters.
    :return: Standard json response for APIs
    :rtype: json
    """

    result = {}

    if value is not None:
        result.update(value)

    if response.get('message', None) is not None:
        result.update({'message': response['message']})

    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors': error})

    if pagination is not None:
        result.update({'pagination': pagination})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask REST API'})

    return make_response(jsonify(result), response['http_code'], headers)
