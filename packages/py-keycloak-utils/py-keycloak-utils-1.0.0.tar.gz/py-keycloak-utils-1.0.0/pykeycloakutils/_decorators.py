import logging
from functools import wraps

from flask import make_response, request
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError



def flask_keycloak_authenticate(oidc: KeycloakOpenID):
    """
    Method to be used as decorator, which accepts instance of KeycloakOpenID
    :param oidc: KeycloakOpenID
    :return: Error message | original function
    """
    def funct_decorator(org_function):
        @wraps(org_function)
        def authorize(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                logging.error("Bearer Token was not found.")
                return make_response("Token is missing", 401)
            try:
                token = token.replace("Bearer ", "")
                oidc.userinfo(token)
                return org_function(*args, **kwargs)
            except KeycloakError as e:
                logging.error(f"Error: {type(e).__name__} Status code: {e.response_code}")
                return make_response(type(e).__name__, e.response_code)

        return authorize

    return funct_decorator
